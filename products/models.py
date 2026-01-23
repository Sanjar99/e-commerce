from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


# -------------------------
# Base mixin
# -------------------------
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# -------------------------
# Category (tree)
# -------------------------
class Category(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children"
    )
    is_active = models.BooleanField(default=True)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ("ordering", "name")
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["parent"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            i = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# -------------------------
# Brand (optional but useful)
# -------------------------
class Brand(TimeStampedModel):
    name = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            i = 1
            while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# -------------------------
# Product (catalog)
# -------------------------
class Product(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # IMPORTANT: category delete productlarni o‘chirib yubormasin
        related_name="products"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0)   # 0.00 - 5.00
    rating_count = models.PositiveIntegerField(default=0)

    # flexible specs for filter/search later
    attributes = models.JSONField(default=dict, blank=True)  # {"material":"cotton","gender":"men"}

    class Meta:
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status"]),
            models.Index(fields=["category"]),
            models.Index(fields=["brand"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            i = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# -------------------------
# Product images (multiple + main)
# -------------------------
class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images/")
    alt_text = models.CharField(max_length=180, blank=True)
    is_main = models.BooleanField(default=False)
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("ordering", "-is_main")
        indexes = [
            models.Index(fields=["product", "is_main"]),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # faqat bitta main bo‘lsin
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).exclude(pk=self.pk).update(is_main=False)

    def __str__(self):
        return f"Image({self.product_id})"


# -------------------------
# Marketplace Offer (Seller listing)
# -------------------------
class SellerProduct(TimeStampedModel):
    """
    Amazon'dagi offer/listing:
    - bir Product'ni bir nechta seller sotishi mumkin
    - narx/holat/sellerga tegishli data shu yerda
    """
    seller = models.ForeignKey("seller.Seller", on_delete=models.CASCADE, related_name="offers")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="offers")

    is_active = models.BooleanField(default=True)

    # offer-level default price (variantda override bo'lishi ham mumkin)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    currency = models.CharField(max_length=6, default="USD")
    seller_sku_prefix = models.CharField(max_length=40, blank=True, null=True)  # optional

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["seller", "product"], name="uniq_seller_product_offer")
        ]
        indexes = [
            models.Index(fields=["seller"]),
            models.Index(fields=["product"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.product.title} @ {getattr(self.seller, 'shop_name', self.seller_id)}"


# -------------------------
# Variant options (Color/Size/Storage...) per product
# -------------------------
class ProductOption(TimeStampedModel):
    """
    Option name: Color, Size, Storage, Material, etc.
    Per-product options (Amazon listing pages show options per product).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=60)  # e.g. "Color"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["product", "name"], name="uniq_product_option_name")
        ]
        indexes = [
            models.Index(fields=["product"]),
        ]

    def __str__(self):
        return f"{self.product_id}:{self.name}"


class ProductOptionValue(TimeStampedModel):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=80)  # e.g. "Black"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["option", "value"], name="uniq_option_value")
        ]
        indexes = [
            models.Index(fields=["option"]),
        ]

    def __str__(self):
        return f"{self.option.name}={self.value}"


# -------------------------
# SKU Variant (real sellable unit)
# -------------------------
class ProductVariant(TimeStampedModel):
    """
    Bitta variant = bitta SKU (Color+Size+Storage kombinatsiyasi)
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=64, unique=True)

    is_active = models.BooleanField(default=True)

    # variant-level media or barcode can be added later
    barcode = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.sku


class VariantSelection(models.Model):
    """
    Variant -> (Option, Value) mapping
    Example:
      Variant SKU123 has:
        Color=Black
        Size=L
    """
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="selections")
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    value = models.ForeignKey(ProductOptionValue, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            # bitta variantda bitta option faqat bir marta
            models.UniqueConstraint(fields=["variant", "option"], name="uniq_variant_option"),
        ]
        indexes = [
            models.Index(fields=["variant"]),
            models.Index(fields=["option"]),
            models.Index(fields=["value"]),
        ]

    def clean(self):
        # value shu option ga tegishli bo‘lishi shart
        if self.value.option_id != self.option_id:
            raise ValidationError("Selected value does not belong to the given option.")

        # option shu variant.product ga tegishli bo‘lishi shart
        if self.option.product_id != self.variant.product_id:
            raise ValidationError("Option does not belong to the variant's product.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.variant.sku}: {self.option.name}={self.value.value}"


# -------------------------
# Offer per SKU (seller price per variant) + inventory
# -------------------------
class SellerVariantOffer(TimeStampedModel):
    """
    Amazon’da: seller har bir SKU uchun narx/stock (ba'zan variant bo'yicha farq qiladi)
    """
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, related_name="variant_offers")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="seller_offers")

    price = models.DecimalField(max_digits=12, decimal_places=2)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["seller_product", "variant"], name="uniq_seller_offer_variant")
        ]
        indexes = [
            models.Index(fields=["variant"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.variant.sku} offer ({self.seller_product_id})"


class Inventory(TimeStampedModel):
    """
    Stock har doim SKU-level bo'lsin.
    Marketplace’da sellerga bog‘lab qo‘yamiz (seller_offer -> inventory).
    """
    seller_variant_offer = models.OneToOneField(
        SellerVariantOffer, on_delete=models.CASCADE, related_name="inventory"
    )
    quantity = models.IntegerField(default=0)
    reserved = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["quantity"]),
        ]

    @property
    def available(self):
        return max(self.quantity - self.reserved, 0)

    def __str__(self):
        return f"Inv({self.seller_variant_offer_id})={self.quantity}"


# -------------------------
# Moderation (seller listing approval)
# -------------------------
class ProductModeration(TimeStampedModel):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    seller_product = models.OneToOneField(
        SellerProduct,
        on_delete=models.CASCADE,
        related_name="moderation"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    staff = models.ForeignKey("staff.StaffUser", on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Moderation({self.seller_product_id})={self.status}"


# -------------------------
# Search keywords (optional)
# -------------------------
class SearchKeyword(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="keywords")
    keyword = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["product", "keyword"], name="uniq_product_keyword")
        ]
        indexes = [
            models.Index(fields=["keyword"]),
        ]

    def __str__(self):
        return self.keyword
