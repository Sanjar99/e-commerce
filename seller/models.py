from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# -------------------------
#   SELLER
#       Vazifasi: Marketplace’dagi sotuvchi hisobini ifodalaydi.
#       Nima uchun kerak: Har bir seller platformaga bog‘lanadi, o‘z do‘konini yaratadi, tavsif, logo va reyting kabi ma’lumotlarni saqlaydi.
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

# -------------------------
#   SellerBalance
#       Vazifasi: Sotuvchining hisob-kitob balansini saqlaydi.
#       Nima uchun kerak: Sellerning jami balansini va hali chiqarilmagan summani kuzatish uchun.
# -------------------------

class SellerBalance(models.Model):
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pending_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.seller.shop_name} balance"
# -------------------------
#   SellerPayout Approval
#       Vazifasi:Seller pul yechish (payout) so‘rovlarini saqlaydi.
#       Nima uchun kerak:Qaysi seller qancha so‘raganini, holati (pending, approved, rejected, paid) va vaqtini kuzatish uchun, processed_at staff tomonidan qayta ishlangan vaqtni saqlaydi.
# -------------------------
class SellerPayout(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    PAID = 'Paid'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (PAID, 'Paid'),
    ]
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    staff = models.ForeignKey('staff.StaffUser', on_delete=models.SET_NULL, null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.seller.shop_name} - {self.status}"
# -------------------------
#   SellerVerification
#       Vazifasi:Sellerning hujjatlarini tasdiqlash jarayoni.
#       Nima uchun kerak:Marketplace’da faqat tasdiqlangan sellerlar faol bo‘lishi uchun; staff tomonidan tekshirish va audit qilish mumkin.
#       Qo'shimcha:StaffUser bilan bog‘langan, shuning uchun kim tasdiqlaganini ko‘rish mumkin.
# -------------------------
class SellerVerification(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    staff = models.ForeignKey('staff.StaffUser', on_delete=models.SET_NULL, null=True, blank=True)
    document = models.FileField(upload_to='seller_documents/')
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

