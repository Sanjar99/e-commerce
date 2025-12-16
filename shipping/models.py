from django.db import models

from orders.models import OrderSellerGroup
# -------------------------
# ShippingProvider
#       Vazifasi: Yetkazib beruvchi kompaniyalarni saqlaydi (kargo xizmati).
#       Nima uchun kerak: Turli delivery xizmatlari bilan ishlash uchun (DHL, FedEx, UzPost va h.k.).
#           tracking_url orqali foydalanuvchi yukni online kuzatishi mumkin.
# -------------------------
class ShippingProvider(models.Model):
    name = models.CharField(max_length=255)
    tracking_url = models.URLField(blank=True, null=True)

# -------------------------
# Delivery
#       Vazifasi: Har bir seller uchun yetkazib berish (shipment) ma’lumotlarini saqlaydi.
#       Nima uchun kerak:Marketplace’da 1 order → bir nechta seller → bir nechta delivery bo‘lishi mumkin.
#               OrderSellerGroup bilan bog‘lanib, har sellerning alohida yetkazib berishini kuzatish uchun.
# -------------------------
class Delivery(models.Model):
    ordersellergroup = models.ForeignKey(OrderSellerGroup, on_delete=models.CASCADE)
    provider = models.ForeignKey(ShippingProvider, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')
    updated_at = models.DateTimeField(auto_now=True)
