from rest_framework import serializers
from .models import (
    Category, Product, ProductImage, ProductAttribute, SearchKeyword,
    SellerProduct, ProductVariant, SellerProductVariantPrice, ProductModeration
)

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
# ProductImage Serializer
# ------------------------------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']
        read_only_fields = ['id']


# ------------------------------
# ProductAttribute Serializer
# ------------------------------
class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'key', 'value']
        read_only_fields = ['id']


# ------------------------------
# SearchKeyword Serializer
# ------------------------------
class SearchKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchKeyword
        fields = ['id', 'keyword']
        read_only_fields = ['id']


# ------------------------------
# Product Serializer (Nested create/update)
# ------------------------------
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    images = ProductImageSerializer(many=True, required=False)
    attributes = ProductAttributeSerializer(many=True, required=False)
    keywords = SearchKeywordSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'category', 'name', 'slug', 'description', 'price',
            'main_image', 'brand', 'stock', 'rating', 'is_active',
            'created_at', 'images', 'attributes', 'keywords'
        ]
        read_only_fields = ['id', 'slug', 'created_at']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        attributes_data = validated_data.pop('attributes', [])
        keywords_data = validated_data.pop('keywords', [])

        product = Product.objects.create(**validated_data)

        for image in images_data:
            ProductImage.objects.create(product=product, **image)

        for attr in attributes_data:
            ProductAttribute.objects.create(product=product, **attr)

        for kw in keywords_data:
            SearchKeyword.objects.create(product=product, **kw)

        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        attributes_data = validated_data.pop('attributes', [])
        keywords_data = validated_data.pop('keywords', [])

        # Update main product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update nested images
        if images_data:
            instance.images.all().delete()
            for image in images_data:
                ProductImage.objects.create(product=instance, **image)

        # Update nested attributes
        if attributes_data:
            instance.attributes.all().delete()
            for attr in attributes_data:
                ProductAttribute.objects.create(product=instance, **attr)

        # Update nested keywords
        if keywords_data:
            instance.keywords.all().delete()
            for kw in keywords_data:
                SearchKeyword.objects.create(product=instance, **kw)

        return instance


# ------------------------------
# SellerProductVariantPrice Serializer
# ------------------------------
class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'type', 'value']
        read_only_fields = ['id']


class SellerProductVariantPriceSerializer(serializers.ModelSerializer):
    variant = ProductVariantSerializer()

    class Meta:
        model = SellerProductVariantPrice
        fields = ['id', 'variant', 'price', 'stock']
        read_only_fields = ['id', 'variant']


# ------------------------------
# SellerProduct Serializer (Nested variant_prices)
# ------------------------------
class SellerProductSerializer(serializers.ModelSerializer):
    variant_prices = SellerProductVariantPriceSerializer(many=True, required=False)
    product = ProductSerializer()

    class Meta:
        model = SellerProduct
        fields = ['id', 'product', 'seller', 'price', 'old_price', 'stock', 'sku', 'is_active', 'variant_prices']
        read_only_fields = ['id']

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        variant_prices_data = validated_data.pop('variant_prices', [])

        # Create or update nested product
        product_serializer = ProductSerializer(data=product_data)
        product_serializer.is_valid(raise_exception=True)
        product = product_serializer.save()

        seller_product = SellerProduct.objects.create(product=product, **validated_data)

        # Nested variant prices
        for vp in variant_prices_data:
            variant_data = vp.pop('variant')
            variant_obj, _ = ProductVariant.objects.get_or_create(product=product, **variant_data)
            SellerProductVariantPrice.objects.create(seller_product=seller_product, variant=variant_obj, **vp)

        return seller_product

    def update(self, instance, validated_data):
        product_data = validated_data.pop('product', None)
        variant_prices_data = validated_data.pop('variant_prices', [])

        # Update main fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update nested product
        if product_data:
            product_serializer = ProductSerializer(instance.product, data=product_data, partial=True)
            product_serializer.is_valid(raise_exception=True)
            product_serializer.save()

        # Update variant prices
        if variant_prices_data:
            instance.variant_prices.all().delete()
            for vp in variant_prices_data:
                variant_data = vp.pop('variant')
                variant_obj, _ = ProductVariant.objects.get_or_create(product=instance.product, **variant_data)
                SellerProductVariantPrice.objects.create(seller_product=instance, variant=variant_obj, **vp)

        return instance
