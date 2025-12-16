from django.db import models
from django.utils.text import slugify

from seller.models import Seller
from staff.models import StaffUser


# -------------------------
#   Category
#       Vazifasi: Productlarni turkumlarga ajratadi (category/subcategory).
#       Nima uchun kerak: Filtrlash, navigatsiya va katalog tizimi uchun.
#       Qiziq nuqta: parent orqali o‘z-o‘ziga bog‘lanadi → subcategory yaratish mumkin.
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
#   Product
#       Vazifasi: Marketplace’dagi asosiy product item.
#       Nima uchun kerak: Har bir seller productni shu asosiy itemga bog‘laydi;
#       umumiy ma’lumotlar (name, description, brand, main_image) shu yerda saqlanadi.
# -------------------------

class Product(models.Model):
    seller = models.ForeignKey('seller.Seller', on_delete=models.CASCADE, related_name='products')
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

# -------------------------
#   ProductImage
#       Vazifasi:Productga bir nechta rasm qo‘shish.
#       Nima uchun kerak: Multiple image support; is_main orqali asosiy rasmni belgilash mumkin.
# -------------------------

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} image"

# -------------------------
#   SellerProduct
#       Vazifasi: Har sellerning o‘z narxi, stock va SKU bilan producti.
#       Nima uchun kerak: Marketplace’da bir productni bir nechta seller sotishi mumkin; har seller uchun alohida narx va stock.
# -------------------------
class SellerProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='seller_products')
    seller = models.ForeignKey('seller.Seller', on_delete=models.CASCADE, related_name='products_seller')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.seller.shop_name}"

# -------------------------
#   ProductVariant
#       Vazifasi: Product variantlarini (Color, Size, Storage) saqlaydi.
#       Nima uchun kerak: Masalan, XL, L yoki 256GB variantlarini boshqarish uchun.
# -------------------------
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

# -------------------------
#   SellerProductVariantPrice
#       Vazifasi: Har seller variant narxi va stock’ini saqlaydi.
#       Nima uchun kerak: Amazon kabi: bir sellerda XL variant qimmat, boshqasida arzon bo‘lishi mumkin.
# -------------------------
class SellerProductVariantPrice(models.Model):
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, related_name='variant_prices')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.seller_product} - {self.variant.value}"

# -------------------------
# ProductAttribute
#       Vazifasi: Productning statik xususiyatlarini saqlaydi (RAM, Material, Size).
#       Nima uchun kerak: Dynamic specs; filtrlar va product info uchun.
# -------------------------
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    key = models.CharField(max_length=100)   # e.g. "RAM", "Material"
    value = models.CharField(max_length=255) # e.g. "8GB", "Cotton"
# -------------------------
# ProductModeration
#       Vazifasi: Productni seller joylagandan keyin admin/ staff tomonidan tasdiqlash jarayoni.
#       Nima uchun kerak: Marketplace’da content moderation; status orqali product qabul qilingan, rad qilingan yoki pending ekanini kuzatadi.
# -------------------------
class ProductModeration(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey('seller.Seller', on_delete=models.CASCADE, related_name='products_moderation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    staff = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# -------------------------
# SearchKeyword Queue
#       Vazifasi:Product uchun search keywords saqlaydi.
#       Nima uchun kerak: SEO va search engine optimization, productni tez topish uchun.
# -------------------------
class SearchKeyword(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='keywords')
    keyword = models.CharField(max_length=100)
