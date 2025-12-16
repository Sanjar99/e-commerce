from rest_framework import serializers
from .models import AnalyticsDaily, RecentlyViewed
from products.serializers import ProductSerializer
from accounts.serializers import UserSerializer  # agar UserSerializer oldin yozilgan bo'lsa

# ------------------------------
# AnalyticsDaily Serializer
# ------------------------------
class AnalyticsDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsDaily
        fields = ['id', 'date', 'users_count', 'orders_count', 'revenue', 'seller_count', 'new_products']
        read_only_fields = ['id', 'users_count', 'orders_count', 'revenue', 'seller_count', 'new_products']
        # read_only_fields ni qo'yish orqali bu serializer faqat display uchun ishlaydi
        # agar backend avtomatik hisobotlarni hisoblaydi, foydalanuvchi update qila olmaydi


# ------------------------------
# RecentlyViewed Serializer
# ------------------------------
class RecentlyViewedSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # nested user ma'lumotlarini ko'rsatadi
    product = ProductSerializer(read_only=True)  # nested product ma'lumotlarini ko'rsatadi

    class Meta:
        model = RecentlyViewed
        fields = ['id', 'user', 'product', 'viewed_at']
        read_only_fields = ['id', 'user', 'product', 'viewed_at']

    # Agar frontend faqat product_id yuborsa va user request.user bo'lsa:
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        product = validated_data.get('product')
        recently_viewed = RecentlyViewed.objects.create(user=user, product=product)
        return recently_viewed
