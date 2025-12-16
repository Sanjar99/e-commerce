from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer
from seller.serializers import SellerSerializer

# ------------------------------
# Notification Serializer
# ------------------------------
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    seller = SellerSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.all(), source='user', write_only=True, required=False
    )
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=SellerSerializer.Meta.model.objects.all(), source='seller', write_only=True, required=False
    )

    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'seller', 'user_id', 'seller_id',
            'title', 'message', 'type', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'seller', 'created_at']

    def create(self, validated_data):
        return Notification.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.message = validated_data.get('message', instance.message)
        instance.type = validated_data.get('type', instance.type)
        instance.is_read = validated_data.get('is_read', instance.is_read)
        instance.save()
        return instance
