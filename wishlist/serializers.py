from rest_framework import serializers
from .models import Wishlist, WishlistItem
from accounts.serializers import UserSerializer
from products.serializers import ProductSerializer

# ------------------------------
# WishlistItem Serializer
# ------------------------------
class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductSerializer.Meta.model.objects.all(),
        source='product', write_only=True
    )

    class Meta:
        model = WishlistItem
        fields = ['id', 'product', 'product_id']
        read_only_fields = ['id', 'product']

# ------------------------------
# Wishlist Serializer (Nested items)
# ------------------------------
class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = WishlistItemSerializer(many=True, required=False)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'items']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        request = self.context.get('request')
        user = request.user if request else None
        wishlist = Wishlist.objects.create(user=user, **validated_data)

        for item_data in items_data:
            WishlistItem.objects.create(wishlist=wishlist, **item_data)

        return wishlist

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', [])
        instance.save()

        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                WishlistItem.objects.create(wishlist=instance, **item_data)

        return instance
