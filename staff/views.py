from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from .models import StaffRole, StaffUser, ModerationLog
from .serializers import StaffRoleSerializer, StaffUserSerializer, ModerationLogSerializer

class StaffRoleViewSet(viewsets.ModelViewSet):
    queryset = StaffRole.objects.all()
    serializer_class = StaffRoleSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class StaffUserViewSet(viewsets.ModelViewSet):
    queryset = StaffUser.objects.select_related('user', 'role').all()
    serializer_class = StaffUserSerializer
    permission_classes = [IsAdminUser]

class ModerationLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModerationLog.objects.select_related('staff').all()
    serializer_class = ModerationLogSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'action_type']
