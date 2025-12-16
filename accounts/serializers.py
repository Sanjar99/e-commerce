from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

# ------------------------------
# User Serializer
# ------------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'avatar', 'is_seller', 'is_staff_user', 'password'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.password = make_password(password)  # Passwordni hash qiladi
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.password = make_password(password)  # Password yangilansa ham hash qilinadi
        instance.save()
        return instance

