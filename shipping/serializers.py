from rest_framework import serializers
from .models import ShippingProvider, Delivery
from orders.serializers import OrderSellerGroupSerializer

# ------------------------------
# ShippingProvider Serializer
# ------------------------------
class ShippingProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingProvider
        fields = ['id', 'name', 'tracking_url']
        read_only_fields = ['id']

# ------------------------------
# Delivery Serializer
# ------------------------------
class DeliverySerializer(serializers.ModelSerializer):
    provider = ShippingProviderSerializer(read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=ShippingProvider.objects.all(), source='provider', write_only=True
    )
    ordersellergroup = OrderSellerGroupSerializer(read_only=True)
    ordersellergroup_id = serializers.PrimaryKeyRelatedField(
        queryset=OrderSellerGroupSerializer.Meta.model.objects.all(), source='ordersellergroup', write_only=True
    )

    class Meta:
        model = Delivery
        fields = ['id', 'ordersellergroup', 'ordersellergroup_id', 'provider', 'provider_id', 'tracking_number', 'status', 'updated_at']
        read_only_fields = ['id', 'ordersellergroup', 'provider', 'updated_at']

    def create(self, validated_data):
        return Delivery.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
