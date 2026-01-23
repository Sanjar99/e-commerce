from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category, Brand, Product, ProductImage,
    ProductOption, ProductOptionValue,
    ProductVariant, VariantSelection,
    SellerProduct, SellerVariantOffer, Inventory,
    ProductModeration, SearchKeyword
)


# -------------------------
# Category
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "is_active", "ordering", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    ordering = ("ordering", "name")
    prepopulated_fields = {"slug": ("name",)}


# -------------------------
# Brand
# -------------------------
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


# -------------------------
# Product Inlines
# -------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "preview", "alt_text", "is_main", "ordering")
    readonly_fields = ("preview",)
    ordering = ("ordering", "-is_main")

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" width="48" height="48" style="object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )
        return "—"
    preview.short_description = "Preview"


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1
    fields = ("name",)
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category", "brand", "status", "rating_avg", "rating_count", "created_at")
    list_filter = ("status", "category", "brand")
    search_fields = ("title", "slug", "description")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ProductImageInline, ProductOptionInline)


# -------------------------
# Option + Values
# -------------------------
class ProductOptionValueInline(admin.TabularInline):
    model = ProductOptionValue
    extra = 1
    fields = ("value",)


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "created_at")
    list_filter = ("name",)
    search_fields = ("name", "product__title")
    inlines = (ProductOptionValueInline,)
    autocomplete_fields = ("product",)


@admin.register(ProductOptionValue)
class ProductOptionValueAdmin(admin.ModelAdmin):
    list_display = ("option", "value", "created_at")
    search_fields = ("option__name", "value", "option__product__title")
    autocomplete_fields = ("option",)


# -------------------------
# Variant + Selections
# -------------------------
class VariantSelectionInline(admin.TabularInline):
    model = VariantSelection
    extra = 1
    fields = ("option", "value")
    autocomplete_fields = ("option", "value")


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("sku", "product", "is_active", "barcode", "created_at")
    list_filter = ("is_active",)
    search_fields = ("sku", "product__title", "product__slug")
    ordering = ("-created_at",)
    autocomplete_fields = ("product",)
    inlines = (VariantSelectionInline,)


# -------------------------
# Marketplace Offer (SellerProduct)
# -------------------------
class InventoryInline(admin.StackedInline):
    model = Inventory
    extra = 0
    fields = ("quantity", "reserved")
    readonly_fields = ()


class SellerVariantOfferInline(admin.TabularInline):
    model = SellerVariantOffer
    extra = 1
    fields = ("variant", "price", "old_price", "is_active")
    autocomplete_fields = ("variant",)
    show_change_link = True


@admin.register(SellerProduct)
class SellerProductAdmin(admin.ModelAdmin):
    list_display = ("id", "seller", "product", "is_active", "price", "currency", "created_at")
    list_filter = ("is_active", "currency")
    search_fields = ("product__title", "product__slug", "seller__shop_name")
    ordering = ("-created_at",)
    autocomplete_fields = ("seller", "product")
    inlines = (SellerVariantOfferInline,)


@admin.register(SellerVariantOffer)
class SellerVariantOfferAdmin(admin.ModelAdmin):
    list_display = ("id", "seller_product", "variant", "price", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("variant__sku", "seller_product__product__title")
    ordering = ("-created_at",)
    autocomplete_fields = ("seller_product", "variant")
    inlines = (InventoryInline,)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("id", "seller_variant_offer", "quantity", "reserved", "available", "created_at")
    search_fields = ("seller_variant_offer__variant__sku",)
    ordering = ("-created_at",)

    def available(self, obj):
        return obj.available
    available.short_description = "Available"


# -------------------------
# Moderation
# -------------------------
@admin.register(ProductModeration)
class ProductModerationAdmin(admin.ModelAdmin):
    list_display = ("seller_product", "status", "staff", "created_at", "updated_at")
    list_filter = ("status",)
    search_fields = ("seller_product__product__title",)
    autocomplete_fields = ("seller_product", "staff")


# -------------------------
# Search Keywords
# -------------------------
@admin.register(SearchKeyword)
class SearchKeywordAdmin(admin.ModelAdmin):
    list_display = ("product", "keyword", "created_at")
    search_fields = ("product__title", "keyword")
    autocomplete_fields = ("product",)
