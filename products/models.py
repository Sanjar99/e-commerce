from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from seller.models import Seller


# -------------------------
#   CATEGORY
# -------------------------

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# -------------------------
#   PRODUCT
# -------------------------

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products_in_category')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    main_image = models.ImageField(upload_to='product_main_images/')
    brand = models.CharField(max_length=255, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} image"


class SellerProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='seller_products')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.seller.shop_name}"


class ProductVariant(models.Model):
    COLOR = "Color"
    SIZE = "Size"
    STORAGE = "Storage"

    VARIANT_TYPE_CHOICES = [
        (COLOR, 'Color'),
        (SIZE, 'Size'),
        (STORAGE, 'Storage')
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    type = models.CharField(max_length=20, choices=VARIANT_TYPE_CHOICES)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product.title} - {self.type}: {self.value}"


class SellerProductVariantPrice(models.Model):
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, related_name='variant_prices')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.seller_product} - {self.variant.value}"
