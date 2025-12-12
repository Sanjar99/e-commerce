from django.db import models
from order.models import OrderSellerGroup

class ShippingProvider(models.Model):
    name = models.CharField(max_length=255)
    tracking_url = models.URLField(blank=True, null=True)

class Delivery(models.Model):
    ordersellergroup = models.ForeignKey(OrderSellerGroup, on_delete=models.CASCADE)
    provider = models.ForeignKey(ShippingProvider, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')
    updated_at = models.DateTimeField(auto_now=True)
