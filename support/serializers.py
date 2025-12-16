from rest_framework import serializers
from .models import SupportTicket
from users.serializers import UserSerializer
from seller.serializers import SellerSerializer
from staff.serializers import StaffUserSerializer

class SupportTicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.all(), source='user', write_only=True
    )
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=SellerSerializer.objects.all(), source='seller', write_only=True, required=False
    )
    assigned_staff = StaffUserSerializer(read_only=True)
    assigned_staff_id = serializers.PrimaryKeyRelatedField(
        queryset=StaffUserSerializer.Meta.model.objects.all(), source='assigned_staff', write_only=True, required=False
    )

    class Meta:
        model = SupportTicket
        fields = ['id', 'user', 'user_id', 'seller', 'seller_id', 'order_id',
                  'subject', 'message', 'status', 'assigned_staff', 'assigned_staff_id', 'created_at']
        read_only_fields = ['id', 'user', 'seller', 'assigned_staff', 'created_at']

    def create(self, validated_data):
        return SupportTicket.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.assigned_staff = validated_data.get('assigned_staff', instance.assigned_staff)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.message = validated_data.get('message', instance.message)
        instance.save()
        return instance
