from rest_framework import serializers
from .models import Review
from accounts.serializers import UserSerializer
from products.serializers import ProductSerializer

# ------------------------------
# Review Serializer
# ------------------------------
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.all(), source='user', write_only=True
    )
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductSerializer.Meta.model.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_id', 'product', 'product_id', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'product', 'created_at']

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance
