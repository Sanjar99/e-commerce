# products/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Product, ProductImage, SellerProduct,
    ProductVariant, SellerProductVariantPrice, ProductAttribute,
    ProductModeration, SearchKeyword
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'product_count')
    list_filter = ('parent',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        return obj.products_in_category.count()

    product_count.short_description = 'Mahsulotlar soni'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'stock', 'rating', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at', 'seller__is_verified')
    search_fields = ('name', 'description', 'brand', 'seller__shop_name')
    list_per_page = 50
    list_select_related = ('seller', 'category')
    readonly_fields = ('created_at', 'rating')
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name', 'slug', 'description', 'category', 'seller', 'brand')
        }),
        ('Narx va miqdor', {
            'fields': ('price', 'stock')
        }),
        ('Status va baho', {
            'fields': ('is_active', 'rating', 'created_at')
        }),
        ('Rasmlar', {
            'fields': ('main_image',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('seller', 'category')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview', 'is_main')
    list_filter = ('is_main', 'product__category')
    search_fields = ('product__name',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "Rasm yo'q"

    image_preview.short_description = 'Rasm'


@admin.register(SellerProduct)
class SellerProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'seller', 'price', 'old_price', 'stock', 'is_active')
    list_filter = ('is_active', 'seller__is_verified')
    search_fields = ('product__name', 'seller__shop_name', 'sku')
    list_select_related = ('product', 'seller')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'seller')


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'type', 'value')
    list_filter = ('type', 'product__category')
    search_fields = ('product__name', 'value')
    list_select_related = ('product',)


@admin.register(SellerProductVariantPrice)
class SellerProductVariantPriceAdmin(admin.ModelAdmin):
    list_display = ('seller_product', 'variant', 'price', 'stock')
    list_filter = ('variant__type',)
    search_fields = ('seller_product__product__name', 'variant__value')
    list_select_related = ('seller_product', 'variant')


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value')
    list_filter = ('key',)
    search_fields = ('product__name', 'key', 'value')
    list_select_related = ('product',)


@admin.register(ProductModeration)
class ProductModerationAdmin(admin.ModelAdmin):
    list_display = ('product', 'seller', 'status', 'staff', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('product__name', 'seller__shop_name', 'reason')
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('product', 'seller', 'staff')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product', 'seller', 'staff')


@admin.register(SearchKeyword)
class SearchKeywordAdmin(admin.ModelAdmin):
    list_display = ('product', 'keyword')
    orders=('product','keyword')
    search_fields = ('product__name', 'keyword')
    list_filter = ('product__category',)
    list_select_related = ('product',)