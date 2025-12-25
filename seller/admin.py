# seller/admin.py
from django.contrib import admin
from .models import Seller


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'is_verified', 'rating', 'product_count', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('shop_name', 'user__username', 'user__email', 'shop_slug')
    list_select_related = ('user',)
    readonly_fields = ('created_at', 'rating')

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = 'Mahsulotlar soni'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')