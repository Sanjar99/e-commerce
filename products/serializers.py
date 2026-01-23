# products/serializers.py
from django.db import transaction
from rest_framework import serializers

from .models import (
    Category, Brand, Product, ProductImage,
    SellerProduct, ProductOption, ProductOptionValue,
    ProductVariant, VariantSelection,
    SellerVariantOffer, Inventory,
    ProductModeration, SearchKeyword
)

# -------------------------
# Category / Brand
# -------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent", "is_active", "ordering", "created_at", "updated_at")
        read_only_fields = ("slug", "created_at", "updated_at")


class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "is_active", "ordering", "children")

    def get_children(self, obj):
        qs = obj.children.filter(is_active=True).order_by("ordering", "name")
        return CategoryTreeSerializer(qs, many=True).data


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ("id", "name", "slug", "created_at", "updated_at")
        read_only_fields = ("slug", "created_at", "updated_at")


# -------------------------
# Product Images
# -------------------------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "alt_text", "is_main", "ordering", "created_at")
        read_only_fields = ("created_at",)


# -------------------------
# Product (Public)
# -------------------------
class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "title", "slug",
            "category", "brand",
            "status",
            "rating_avg", "rating_count",
            "main_image",
            "created_at", "updated_at",
        )

    def get_main_image(self, obj):
        img = obj.images.filter(is_main=True).order_by("ordering").first()
        return ProductImageSerializer(img).data if img else None


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    # options + values
    options = serializers.SerializerMethodField()
    # variants with selections
    variants = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id", "title", "slug",
            "category", "brand",
            "description",
            "status",
            "rating_avg", "rating_count",
            "attributes",
            "images",
            "options",
            "variants",
            "created_at", "updated_at",
        )

    def get_options(self, obj):
        qs = obj.options.all().prefetch_related("values").order_by("name")
        return ProductOptionReadSerializer(qs, many=True).data

    def get_variants(self, obj):
        qs = obj.variants.filter(is_active=True).prefetch_related(
            "selections__option", "selections__value"
        )
        return ProductVariantReadSerializer(qs, many=True).data


# -------------------------
# Product (Admin/Seller create/update)
# -------------------------
class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "category", "brand",
            "title", "description",
            "status",
            "attributes",
        )


# -------------------------
# Options (Color/Size/Storage) per product
# -------------------------
class ProductOptionValueReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOptionValue
        fields = ("id", "value")


class ProductOptionReadSerializer(serializers.ModelSerializer):
    values = ProductOptionValueReadSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOption
        fields = ("id", "name", "values")


class ProductOptionSerializer(serializers.ModelSerializer):
    """
    Create/update option (e.g. Color)
    """
    class Meta:
        model = ProductOption
        fields = ("id", "product", "name")


class ProductOptionValueSerializer(serializers.ModelSerializer):
    """
    Create/update option value (e.g. Black)
    """
    class Meta:
        model = ProductOptionValue
        fields = ("id", "option", "value")


# -------------------------
# Variant (SKU) + selections
# -------------------------
class VariantSelectionReadSerializer(serializers.ModelSerializer):
    option_name = serializers.CharField(source="option.name", read_only=True)
    value_text = serializers.CharField(source="value.value", read_only=True)

    class Meta:
        model = VariantSelection
        fields = ("id", "option", "value", "option_name", "value_text")


class ProductVariantReadSerializer(serializers.ModelSerializer):
    selections = VariantSelectionReadSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ("id", "product", "sku", "is_active", "barcode", "selections", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")


class VariantSelectionWriteSerializer(serializers.Serializer):
    """
    One selection item:
    { "option": 1, "value": 10 }
    """
    option = serializers.IntegerField()
    value = serializers.IntegerField()


class ProductVariantWriteSerializer(serializers.ModelSerializer):
    """
    Create/update SKU with selections.
    """
    selections = VariantSelectionWriteSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = ProductVariant
        fields = ("id", "product", "sku", "is_active", "barcode", "selections")

    def validate_selections(self, items):
        # option duplicate bo'lmasin
        option_ids = [i["option"] for i in items]
        if len(option_ids) != len(set(option_ids)):
            raise serializers.ValidationError("Each option can be selected only once per SKU.")
        return items

    @transaction.atomic
    def create(self, validated_data):
        selections = validated_data.pop("selections", [])
        variant = ProductVariant.objects.create(**validated_data)

        # selections yozish
        for item in selections:
            VariantSelection.objects.create(
                variant=variant,
                option_id=item["option"],
                value_id=item["value"],
            )
        return variant

    @transaction.atomic
    def update(self, instance, validated_data):
        selections = validated_data.pop("selections", None)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        # agar selections kelgan bo'lsa, replace qilamiz
        if selections is not None:
            instance.selections.all().delete()
            for item in selections:
                VariantSelection.objects.create(
                    variant=instance,
                    option_id=item["option"],
                    value_id=item["value"],
                )
        return instance


# -------------------------
# Seller Offer (listing)
# -------------------------
class SellerProductSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    product_slug = serializers.CharField(source="product.slug", read_only=True)

    class Meta:
        model = SellerProduct
        fields = (
            "id",
            "seller", "product",
            "product_title", "product_slug",
            "is_active",
            "price", "old_price", "currency",
            "seller_sku_prefix",
            "created_at", "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class InventorySerializer(serializers.ModelSerializer):
    available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Inventory
        fields = ("id", "quantity", "reserved", "available", "created_at", "updated_at")
        read_only_fields = ("available", "created_at", "updated_at")


class SellerVariantOfferReadSerializer(serializers.ModelSerializer):
    variant_sku = serializers.CharField(source="variant.sku", read_only=True)
    inventory = InventorySerializer(read_only=True)
    variant = ProductVariantReadSerializer(read_only=True)

    class Meta:
        model = SellerVariantOffer
        fields = (
            "id",
            "seller_product",
            "variant",
            "variant_sku",
            "price", "old_price",
            "is_active",
            "inventory",
            "created_at", "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")


class SellerVariantOfferWriteSerializer(serializers.ModelSerializer):
    """
    Create/update seller price per SKU.
    Inventory alohida endpoint/serializer orqali ham qilsa bo'ladi,
    lekin qulaylik uchun bu yerda nested qildim.
    """
    inventory = InventorySerializer(required=False)

    class Meta:
        model = SellerVariantOffer
        fields = (
            "id",
            "seller_product",
            "variant",
            "price", "old_price",
            "is_active",
            "inventory",
        )

    @transaction.atomic
    def create(self, validated_data):
        inv_data = validated_data.pop("inventory", None)
        offer = SellerVariantOffer.objects.create(**validated_data)

        if inv_data is not None:
            Inventory.objects.create(seller_variant_offer=offer, **inv_data)
        else:
            # default inventory yaratib qo'yamiz (optional)
            Inventory.objects.create(seller_variant_offer=offer, quantity=0, reserved=0)

        return offer

    @transaction.atomic
    def update(self, instance, validated_data):
        inv_data = validated_data.pop("inventory", None)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if inv_data is not None:
            inv, _ = Inventory.objects.get_or_create(seller_variant_offer=instance)
            for attr, val in inv_data.items():
                setattr(inv, attr, val)
            inv.save()

        return instance


# -------------------------
# Moderation
# -------------------------
class ProductModerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModeration
        fields = ("id", "seller_product", "status", "staff", "reason", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")


# -------------------------
# Search Keywords
# -------------------------
class SearchKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchKeyword
        fields = ("id", "product", "keyword", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")
