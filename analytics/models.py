from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class AnalyticsDaily(models.Model):
    date = models.DateField()
    users_count = models.PositiveIntegerField(default=0)
    orders_count = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    seller_count = models.PositiveIntegerField(default=0)
    new_products = models.PositiveIntegerField(default=0)


class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
