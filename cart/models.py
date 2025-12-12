from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from products.models import SellerProduct


# -------------------------
#   CART
# -------------------------

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_that_moment = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.seller_product} x{self.quantity}"

