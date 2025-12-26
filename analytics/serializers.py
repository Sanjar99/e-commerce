from django.utils import timezone
from rest_framework import serializers
from products.models import Product
from .models import AnalyticsDaily, RecentlyViewed
from accounts.serializers import UserSerializer

class AnalyticsDailySerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsDaily
        fields = '__all__'
        read_only_fields = '__all__'

class RecentlyViewedSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = RecentlyViewed
        fields = ['id', 'user', 'product', 'viewed_at']
        read_only_fields = ['id', 'user', 'viewed_at']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        obj, created = RecentlyViewed.objects.update_or_create(
            user=user,
            product=product,
            defaults={'viewed_at': timezone.now()}
        )
        return obj
