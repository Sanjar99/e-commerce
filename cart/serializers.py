from rest_framework import serializers

from products.models import SellerProduct
from .models import Cart, CartItem
from products.serializers import SellerProductSerializer
from accounts.serializers import UserSerializer

# ------------------------------
# CartItem Serializer
# ------------------------------
class CartItemSerializer(serializers.ModelSerializer):
    seller_product = SellerProductSerializer(read_only=True)
    seller_product_id = serializers.PrimaryKeyRelatedField(
        queryset=SellerProduct.objects.all(), source='seller_product', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'seller_product', 'seller_product_id', 'quantity', 'price_at_that_moment']
        read_only_fields = ['id', 'price_at_that_moment', 'seller_product']

    def create(self, validated_data):
        seller_product = validated_data['seller_product']
        validated_data['price_at_that_moment'] = seller_product.price
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        # Narx o'zgarmaydi, faqat quantity update qilinadi
        instance.save()
        return instance


# ------------------------------
# Cart Serializer (Nested items)
# ------------------------------
class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = CartItemSerializer(many=True, required=False)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']
        read_only_fields = ['id', 'created_at', 'user']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        request = self.context.get('request')
        user = request.user if request else None
        cart = Cart.objects.create(user=user, **validated_data)

        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)

        return cart

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.save()

        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                CartItem.objects.create(cart=instance, **item_data)

        return instance
