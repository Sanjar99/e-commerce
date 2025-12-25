from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import StaffRole, StaffUser, ModerationLog, SupportTicket

from .serializers import (
    StaffRoleSerializer,
    StaffUserSerializer,
    ModerationLogSerializer,
    SupportTicketSerializer
)
from services.permissions import (
    IsSuperAdmin,
    IsStaffOrOwner,
    IsProductModeratorOrSuperAdmin
)


# ------------------------------
# StaffRole ViewSet
# ------------------------------
class StaffRoleViewSet(viewsets.ModelViewSet):
    queryset = StaffRole.objects.all()
    serializer_class = StaffRoleSerializer
    permission_classes = [IsSuperAdmin]  # Faqat super admin CRUD qilishi mumkin


# ------------------------------
# StaffUser ViewSet
# ------------------------------
class StaffUserViewSet(viewsets.ModelViewSet):
    serializer_class = StaffUserSerializer
    permission_classes = [IsSuperAdmin]  # Faqat super admin barcha stafflarni boshqaradi

    def get_queryset(self):
        return (
            StaffUser.objects
            .select_related('user', 'role')
            .prefetch_related('assigned_categories', 'assigned_sellers')
        )


# ------------------------------
# ModerationLog ViewSet
# ------------------------------
class ModerationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Loglar faqat o‘qish uchun, Product Moderator va Super Admin ko‘rishi mumkin
    """
    serializer_class = ModerationLogSerializer
    permission_classes = [IsProductModeratorOrSuperAdmin]

    def get_queryset(self):
        return (
            ModerationLog.objects
            .select_related('staff__user', 'staff__role')
        )
    # Filter, search, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action_type', 'target_type', 'staff__role__name', 'staff__user__username']
    search_fields = ['note', 'staff__user__username']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

# ------------------------------
# SupportTicket ViewSet
# ------------------------------
class SupportTicketViewSet(viewsets.ModelViewSet):
    serializer_class = SupportTicketSerializer
    permission_classes = [IsStaffOrOwner]  # Staff = hamma ticket, oddiy user = o‘z ticketi

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'assigned_staff__user__username', 'user__username', 'seller__shop_name']
    search_fields = ['subject', 'message']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = (
            SupportTicket.objects
            .select_related(
                'user',
                'seller',
                'assigned_staff__user',
                'assigned_staff__role'
            )
        )

        # Oddiy user faqat o‘z ticketini ko‘radi
        if not hasattr(self.request.user, 'staffuser'):
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        """
        Oddiy user ticket ochsa user = request.user
        Staff esa assigned_staff bilan ochadi
        """
        if hasattr(self.request.user, 'staffuser'):
            serializer.save(assigned_staff=self.request.user.staffuser)
        else:
            serializer.save(user=self.request.user)