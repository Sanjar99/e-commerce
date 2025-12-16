from rest_framework import serializers
from .models import Seller, SellerBalance, SellerPayout, SellerVerification
from accounts.serializers import UserSerializer
from staff.models import StaffUser

# ------------------------------
# Seller Serializer
# ------------------------------
class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSerializer.Meta.model.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = Seller
        fields = [
            'id', 'user', 'user_id', 'shop_name', 'shop_slug',
            'description', 'logo', 'is_verified', 'rating', 'created_at'
        ]
        read_only_fields = ['id', 'shop_slug', 'created_at', 'rating', 'is_verified']

# ------------------------------
# SellerBalance Serializer
# ------------------------------
class SellerBalanceSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all(),
        source='seller',
        write_only=True
    )

    class Meta:
        model = SellerBalance
        fields = ['id', 'seller', 'seller_id', 'balance', 'pending_amount', 'last_update']
        read_only_fields = ['id', 'seller', 'last_update']

# ------------------------------
# SellerPayout Serializer
# ------------------------------
class SellerPayoutSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all(),
        source='seller',
        write_only=True
    )
    staff = serializers.StringRelatedField(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=StaffUser.objects.all(),
        source='staff',
        write_only=True,
        required=False
    )

    class Meta:
        model = SellerPayout
        fields = ['id', 'seller', 'seller_id', 'amount', 'status', 'staff', 'staff_id', 'requested_at', 'processed_at']
        read_only_fields = ['id', 'seller', 'staff', 'requested_at']

# ------------------------------
# SellerVerification Serializer
# ------------------------------
class SellerVerificationSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all(),
        source='seller',
        write_only=True
    )
    staff = serializers.StringRelatedField(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(
        queryset=StaffUser.objects.all(),
        source='staff',
        write_only=True,
        required=False
    )

    class Meta:
        model = SellerVerification
        fields = [
            'id', 'seller', 'seller_id', 'status', 'staff', 'staff_id',
            'document', 'reason', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'seller', 'staff', 'created_at', 'updated_at']
