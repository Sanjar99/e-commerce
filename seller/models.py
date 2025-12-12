from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# -------------------------
#   SELLER
# -------------------------

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=255)
    shop_slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="seller/logos/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.shop_slug:
            self.shop_slug = slugify(self.shop_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.shop_name


class SellerBalance(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pending_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.seller.shop_name} balance"

class SellerPayout(models.Model):
    PENDING = "Pending"
    PAID = "Paid"
    REJECTED = "Rejected"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (PAID, "Paid"),
        (REJECTED, "Rejected"),
    ]
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payout {self.id} - {self.seller.shop_name} — {self.amount} — {self.status}"

