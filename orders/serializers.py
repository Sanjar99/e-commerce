from rest_framework import serializers
from .models import Address, Order, OrderSellerGroup, OrderItem
from accounts.serializers import UserSerializer
from products.serializers import SellerProductSerializer
from seller.models import Seller  # serializer emas, modelni ishlatamiz

# ------------------------------
# Address Serializer
# ------------------------------
class AddressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = Address
        fields = ['id', 'user', 'user_id', 'street', 'district', 'city', 'postal_code', 'is_default']
        read_only_fields = ['id', 'user']

# ------------------------------
# OrderItem Serializer
# ------------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    seller_product = SellerProductSerializer(read_only=True)
    seller_product_id = serializers.PrimaryKeyRelatedField(
        queryset=SellerProductSerializer.Meta.model.objects.all(),
        source='seller_product',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'seller_product', 'seller_product_id', 'quantity', 'price']
        read_only_fields = ['id', 'price']

# ------------------------------
# OrderSellerGroup Serializer
# ------------------------------
class OrderSellerGroupSerializer(serializers.ModelSerializer):
    seller = serializers.StringRelatedField(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all(),  # <- modelga bog'landi
        source='seller',
        write_only=True
    )
    items = OrderItemSerializer(many=True)

    class Meta:
        model = OrderSellerGroup
        fields = ['id', 'seller', 'seller_id', 'seller_total_price', 'status', 'items']
        read_only_fields = ['id', 'seller_total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        group = OrderSellerGroup.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(seller_group=group, **item_data)
        return group

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

# ------------------------------
# Order Serializer
# ------------------------------
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.all(),
        source='user',
        write_only=True
    )
    shipping_address = AddressSerializer(read_only=True)
    shipping_address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(),
        source='shipping_address',
        write_only=True
    )
    seller_groups = OrderSellerGroupSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_id', 'order_number', 'total_price', 'total_items',
            'payment_method', 'shipping_address', 'shipping_address_id',
            'status', 'is_paid', 'created_at', 'seller_groups'
        ]
        read_only_fields = ['id', 'total_price', 'total_items', 'is_paid', 'created_at']

    def create(self, validated_data):
        groups_data = validated_data.pop('seller_groups')
        order = Order.objects.create(**validated_data)
        for group_data in groups_data:
            items_data = group_data.pop('items')
            group = OrderSellerGroup.objects.create(order=order, **group_data)
            for item_data in items_data:
                OrderItem.objects.create(seller_group=group, **item_data)
        return order

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.save()
        return instance
