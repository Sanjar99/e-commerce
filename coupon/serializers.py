from rest_framework import serializers
from .models import Coupon
from django.utils import timezone

# ------------------------------
# Coupon Serializer
# ------------------------------
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'discount_type', 'amount',
            'expires_at', 'usage_limit', 'used_count'
        ]
        read_only_fields = ['id', 'used_count']

    def validate_expires_at(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Expiration date must be in the future.")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Discount amount must be positive.")
        return value

    def create(self, validated_data):
        return Coupon.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
