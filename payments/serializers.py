from rest_framework import serializers
from .models import Payment
from orders.serializers import OrderSerializer

# ------------------------------
# Payment Serializer
# ------------------------------
class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=OrderSerializer.Meta.model.objects.all(), source='order', write_only=True
    )

    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_id', 'payment_id', 'amount', 'status', 'paid_at']
        read_only_fields = ['id', 'order', 'paid_at']

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.paid_at = validated_data.get('paid_at', instance.paid_at)
        instance.save()
        return instance
