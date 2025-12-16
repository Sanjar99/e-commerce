from rest_framework import serializers
from .models import (
    Category, Product, ProductImage, SellerProduct, ProductVariant,
    SellerProductVariantPrice, ProductAttribute, ProductModeration, SearchKeyword
)
from seller.models import Seller
from staff.models import StaffUser

# ------------------------------
# Category Serializer
# ------------------------------
class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'subcategories']
        read_only_fields = ['id', 'slug', 'subcategories']

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data

# ------------------------------
# Product Serializer
# ------------------------------
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    attributes = serializers.SerializerMethodField(read_only=True)
    keywords = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'category', 'name', 'slug', 'description', 'price',
            'main_image', 'brand', 'stock', 'rating', 'is_active',
            'created_at', 'images', 'attributes', 'keywords'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'images', 'attributes', 'keywords']

    def get_images(self, obj):
        return ProductImageSerializer(obj.images.all(), many=True).data

    def get_attributes(self, obj):
        return ProductAttributeSerializer(obj.attributes.all(), many=True).data

    def get_keywords(self, obj):
        return SearchKeywordSerializer(obj.keywords.all(), many=True).data

# ------------------------------
# ProductImage Serializer
# ------------------------------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'is_main']
        read_only_fields = ['id']


# ------------------------------
# SellerProduct Serializer
# ------------------------------
class SellerProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant_prices = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SellerProduct
        fields = ['id', 'product', 'seller', 'price', 'old_price', 'stock', 'sku', 'is_active', 'created_at', 'variant_prices']
        read_only_fields = ['id', 'created_at', 'variant_prices']

    def get_variant_prices(self, obj):
        return SellerProductVariantPriceSerializer(obj.variant_prices.all(), many=True).data


# ------------------------------
# ProductVariant Serializer
# ------------------------------
class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'type', 'value']
        read_only_fields = ['id']


# ------------------------------
# SellerProductVariantPrice Serializer
# ------------------------------
class SellerProductVariantPriceSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = SellerProductVariantPrice
        fields = ['id', 'seller_product', 'variant', 'price', 'stock']
        read_only_fields = ['id', 'variant']


# ------------------------------
# ProductAttribute Serializer
# ------------------------------
class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'product', 'key', 'value']
        read_only_fields = ['id']


# ------------------------------
# ProductModeration Serializer
# ------------------------------
class ProductModerationSerializer(serializers.ModelSerializer):
    staff = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProductModeration
        fields = ['id', 'product', 'seller', 'status', 'staff', 'reason', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'staff']


# ------------------------------
# SearchKeyword Serializer
# ------------------------------
class SearchKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchKeyword
        fields = ['id', 'product', 'keyword']
        read_only_fields = ['id']