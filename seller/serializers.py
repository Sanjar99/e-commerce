from rest_framework import serializers
from .models import Seller, SellerBalance, SellerPayout, SellerVerification
from accounts.serializers import UserSerializer
from staff.serializers import StaffUserSerializer

# ------------------------------
# Seller Serializer
# ------------------------------
class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.all(),
        source='user', write_only=True
    )

    class Meta:
        model = Seller
        fields = ['id', 'user', 'user_id', 'shop_name', 'shop_slug', 'description', 'logo', 'is_verified', 'rating', 'created_at']
        read_only_fields = ['id', 'shop_slug', 'created_at', 'rating', 'is_verified']

# ------------------------------
# SellerBalance Serializer
# ------------------------------
class SellerBalanceSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), source='seller', write_only=True)

    class Meta:
        model = SellerBalance
        fields = ['id', 'seller', 'seller_id', 'balance', 'pending_amount', 'last_update']
        read_only_fields = ['id', 'seller', 'last_update']

# ------------------------------
# SellerPayout Serializer
# ------------------------------
class SellerPayoutSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), source='seller', write_only=True)
    staff = StaffUserSerializer(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(queryset=StaffUserSerializer.Meta.model.objects.all(), source='staff', write_only=True, required=False)

    class Meta:
        model = SellerPayout
        fields = ['id', 'seller', 'seller_id', 'amount', 'status', 'staff', 'staff_id', 'requested_at', 'processed_at']
        read_only_fields = ['id', 'seller', 'staff', 'requested_at']

    def create(self, validated_data):
        return SellerPayout.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# ------------------------------
# SellerVerification Serializer
# ------------------------------
class SellerVerificationSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), source='seller', write_only=True)
    staff = StaffUserSerializer(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(queryset=StaffUserSerializer.Meta.model.objects.all(), source='staff', write_only=True, required=False)

    class Meta:
        model = SellerVerification
        fields = ['id', 'seller', 'seller_id', 'status', 'staff', 'staff_id', 'document', 'reason', 'created_at', 'updated_at']
        read_only_fields = ['id', 'seller', 'staff', 'created_at', 'updated_at']

    def create(self, validated_data):
        return SellerVerification.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
