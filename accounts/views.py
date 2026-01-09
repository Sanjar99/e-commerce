from rest_framework import viewsets, filters, status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.tokens import default_token_generator
from djoser import signals
from .serializers import UserSerializer, UserMeSerializer, UpdateProfileSerializer

User = get_user_model()

# ------------------------------
# Custom Permissions
# ------------------------------
class IsAdminOrStaff(BasePermission):
    """
    Faqat admin yoki staff userlar CRUD qilishi mumkin.
    Oddiy userlar kira olmaydi.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_seller)


# ------------------------------
# SuperAdmin user CRUD
# ------------------------------
class AdminUserViewSet(ModelViewSet):
    """
    Faqat SuperAdmin:
    - user list
    - user detail
    - block/unblock
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrStaff]  # SuperAdmin, staff userlar


# ------------------------------
# User Me (Profile) View
# ------------------------------
class UserMeView(APIView):
    """
    /me/ endpoint
    Foydalanuvchi o‘z profile’ini ko‘radi
    """
    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------------------
# Update Profile View
# ------------------------------
class UpdateProfileView(APIView):
    """
    Foydalanuvchi o‘z profile’ini yangilaydi
    """
    def put(self, request):
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------------------
# User Activation View
# ------------------------------
class UserActivateView(APIView):
    """
    User activation using Django token
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
