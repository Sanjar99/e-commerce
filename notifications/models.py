from django.db import models
from django.conf import settings

from seller.models import Seller

# -------------------------
# Notification
#       Vazifasi: User va Sellerlarga yuboriladigan tizim xabarlarini saqlaydi.
#       Nima uchun kerak: Order holati o‘zgarganda xabar berish
#               Payout tasdiqlanganda sellerga bildirish
#               Support yoki promo xabarlarini yuborish
# -------------------------
class Notification(models.Model):
    ORDER = 'Order'
    PAYOUT = 'Payout'
    SUPPORT = 'Support'
    PROMO = 'Promo'

    TYPE_CHOICES = [
        (ORDER, 'Order'),
        (PAYOUT, 'Payout'),
        (SUPPORT, 'Support'),
        (PROMO, 'Promo'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
