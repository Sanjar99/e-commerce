from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import User

# ------------------------------
# User Serializer (READ)
# ------------------------------
class UserSerializer(BaseUserSerializer):
    # is_seller faqat o'qish uchun
    is_seller = serializers.BooleanField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'phone',
            'avatar',
            'is_seller',
        )


# ------------------------------
# User Create Serializer (REGISTRATION)
# ------------------------------
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'phone',
            'password',
            're_password',
        )

    def validate_phone(self, value):
        """Phone majburiy va format to‘g‘ri ekanligini tekshiradi"""
        if not value:
            raise serializers.ValidationError("Phone number is required.")
        return value


# ------------------------------
# User Me Serializer (PROFILE)
# ------------------------------
class UserMeSerializer(serializers.ModelSerializer):
    is_seller = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)  # Staff info faqat o'qish uchun

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'phone',
            'avatar',
            'is_seller',
            'is_staff',
        )


# ------------------------------
# User Update Profile Serializer
# ------------------------------
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'phone',
            'avatar',
        )

    def validate_phone(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required.")
        return value
