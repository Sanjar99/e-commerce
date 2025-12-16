from rest_framework import serializers
from .models import ReturnRequest
from accounts.serializers import UserSerializer
from staff.serializers import StaffUserSerializer
from orders.serializers import OrderItemSerializer

# ------------------------------
# ReturnRequest Serializer
# ------------------------------
class ReturnRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.all(), source='user', write_only=True
    )
    staff = StaffUserSerializer(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=StaffUserSerializer.Meta.model.objects.all(), source='staff', write_only=True, required=False
    )
    order_item = OrderItemSerializer(read_only=True)
    order_item_id = serializers.PrimaryKeyRelatedField(
        queryset=OrderItemSerializer.Meta.model.objects.all(), source='order_item', write_only=True
    )

    class Meta:
        model = ReturnRequest
        fields = ['id', 'order_item', 'order_item_id', 'user', 'user_id', 'reason', 'status', 'staff', 'staff_id', 'created_at']
        read_only_fields = ['id', 'user', 'staff', 'order_item', 'created_at']

    def create(self, validated_data):
        return ReturnRequest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.staff = validated_data.get('staff', instance.staff)
        instance.reason = validated_data.get('reason', instance.reason)
        instance.save()
        return instance
