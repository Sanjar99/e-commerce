from rest_framework import serializers
from .models import StaffRole, StaffUser, ModerationLog, SupportTicket
from accounts.serializers import UserSerializer
from products.models import Category
from seller.models import Seller

# ------------------------------
# StaffRole Serializer
# ------------------------------
class StaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRole
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


# ------------------------------
# StaffUser Serializer
# ------------------------------
class StaffUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = StaffRoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=StaffRole.objects.all(), source='role', write_only=True)
    assigned_categories = serializers.StringRelatedField(many=True, read_only=True)
    assigned_categories_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), source='assigned_categories', write_only=True
    )
    assigned_sellers = serializers.StringRelatedField(many=True, read_only=True)
    assigned_sellers_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Seller.objects.all(), source='staff_assigned_tickets', write_only=True
    )

    class Meta:
        model = StaffUser
        fields = [
            'id', 'user', 'role', 'role_id',
            'assigned_categories', 'assigned_categories_ids',
            'assigned_sellers', 'assigned_sellers_ids',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        assigned_categories = validated_data.pop('assigned_categories', [])
        assigned_sellers = validated_data.pop('assigned_sellers', [])

        staff_user = StaffUser.objects.create(user=user, **validated_data)
        staff_user.assigned_categories.set(assigned_categories)
        staff_user.assigned_sellers.set(assigned_sellers)
        return staff_user

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        assigned_categories = validated_data.pop('assigned_categories', None)
        if assigned_categories is not None:
            instance.assigned_categories.set(assigned_categories)

        assigned_sellers = validated_data.pop('assigned_sellers', None)
        if assigned_sellers is not None:
            instance.assigned_sellers.set(assigned_sellers)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# ------------------------------
# ModerationLog Serializer
# ------------------------------
class ModerationLogSerializer(serializers.ModelSerializer):
    staff = StaffUserSerializer(read_only=True)
    staff_id = serializers.PrimaryKeyRelatedField(queryset=StaffUser.objects.all(), source='staff', write_only=True)

    class Meta:
        model = ModerationLog
        fields = ['id', 'staff', 'staff_id', 'action_type', 'target_type', 'target_id', 'note', 'created_at']
        read_only_fields = ['id', 'staff', 'created_at']


# ------------------------------
# SupportTicket Serializer
# ------------------------------
class SupportTicketSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=UserSerializer.Meta.model.objects.all(), source='user', write_only=True)
    seller = serializers.StringRelatedField(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), source='seller', write_only=True, required=False)
    assigned_staff = StaffUserSerializer(read_only=True)
    assigned_staff_id = serializers.PrimaryKeyRelatedField(queryset=StaffUser.objects.all(), source='assigned_staff', write_only=True, required=False)

    class Meta:
        model = SupportTicket
        fields = [
            'id', 'user', 'user_id', 'seller', 'seller_id',
            'order_id', 'subject', 'message', 'status',
            'assigned_staff', 'assigned_staff_id', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'seller', 'assigned_staff', 'created_at']

    def create(self, validated_data):
        return SupportTicket.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
