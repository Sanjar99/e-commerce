from rest_framework import viewsets, filters, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.views import APIView
from djoser import signals
from djoser.conf import settings as djoser_settings
from djoser.utils import decode_uid
from .models import User
from .serializers import UserSerializer

from django.contrib.auth.tokens import default_token_generator

# ------------------------------
# Custom permission: Admin yoki Staff
# ------------------------------
class IsAdminOrStaff(BasePermission):
    """
    Faqat admin yoki staff userlar CRUD qilishi mumkin.
    Oddiy userlar kira olmaydi.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_seller)


# ------------------------------
# User ViewSet
# ------------------------------
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrStaff]  # faqat admin/staff userlar
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    search_fields = ['username', 'email', 'phone']
    ordering_fields = ['id', 'date_joined']
    ordering = ['-date_joined']  # default: yangi userlar birinchi

    filterset_fields = ['is_active', 'is_seller']  # filter qilish mumkin

    def get_queryset(self):
        """
        Faqat faollashtirilgan userlar:
        - admin xohlagan holatda barcha userlarni ko‘rishi mumkin
        """
        user = self.request.user
        if user.is_staff:
            # Admin: barcha userlarni ko‘radi
            return User.objects.all()
        else:
            # Staff: faqat active userlar
            return User.objects.filter(is_active=True)

    def destroy(self, request, *args, **kwargs):
        """
        Optional: userni soft delete qilish mumkin.
        Hozircha hard delete
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


User = get_user_model()

class UserActivateView(APIView):
    """
    User activation view using default Django token generator.
    """

    def get(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            signals.user_activated.send(sender=self.__class__, user=user, request=request)
            return Response({"detail": "Account activated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)