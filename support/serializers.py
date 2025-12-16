from rest_framework import serializers
from .models import SupportTicket
from accounts.serializers import UserSerializer
from seller.models import Seller
from staff.models import StaffUser


class SupportTicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.all(),
        source='user',
        write_only=True
    )

    seller = serializers.StringRelatedField(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all(),
        source='seller',
        write_only=True,
        required=False
    )

    assigned_staff = serializers.StringRelatedField(read_only=True)
    assigned_staff_id = serializers.PrimaryKeyRelatedField(
        queryset=StaffUser.objects.all(),
        source='assigned_staff',
        write_only=True,
        required=False
    )

    class Meta:
        model = SupportTicket
        fields = [
            'id',
            'user', 'user_id',
            'seller', 'seller_id',
            'order_id',
            'subject',
            'message',
            'status',
            'assigned_staff', 'assigned_staff_id',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
