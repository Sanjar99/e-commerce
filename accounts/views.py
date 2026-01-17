from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.tokens import default_token_generator
from djoser import signals
from .serializers import UserSerializer, UserMeSerializer, UpdateProfileSerializer,AdminUserUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from services.permissions import IsAdminOrStaff
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi
from djoser.views import UserViewSet


User = get_user_model()
# ------------------------------
# # SuperAdmin user CRUD
# # ------------------------------
class AdminUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminOrStaff]
    http_method_names = ['get', 'patch']

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return AdminUserUpdateSerializer
        return UserSerializer

    @swagger_auto_schema(request_body=AdminUserUpdateSerializer)  # ✅ PATCH body majburan chiqadi
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class CustomUserViewSet(UserViewSet):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        consumes=['multipart/form-data'],
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('phone', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('re_password', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('avatar', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),  # ✅ FILE chiqadi
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


# ------------------------------
# User Me (Profile) View
# ------------------------------
class UserMeView(APIView):
    """
    /me/ endpoint
    Foydalanuvchi o‘z profile’ini ko‘radi
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------------------
# Update Profile View
# ------------------------------
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('phone', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('avatar', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False),  # ✅
        ],
        consumes=['multipart/form-data'],
    )
    def patch(self, request):
        serializer = UpdateProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# ------------------------------
# User Activation View
# ------------------------------
class UserActivateView(APIView):
    """
    User account activation via email link.
    URL: /auth/activate/<uid>/<token>/
    """

    authentication_classes = []  # login talab qilinmaydi
    permission_classes = []      # hammaga ochiq (email link)

    def get(self, request, uid, token):
        # 1️⃣ UID decode
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Invalid activation link."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2️⃣ Allaqachon aktiv bo‘lsa
        if user.is_active:
            return Response(
                {"detail": "Account already activated."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3️⃣ Token tekshirish
        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired activation token."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4️⃣ Aktivatsiya
        user.is_active = True
        user.save(update_fields=["is_active"])

        # 5️⃣ Djoser signal (analytics / hooklar uchun)
        signals.user_activated.send(
            sender=self.__class__,
            user=user,
            request=request
        )

        return Response(
            {"detail": "Account activated successfully."},
            status=status.HTTP_200_OK
        )