from django.db import models
from django.contrib.auth.models import User

from products.models import Product


# -------------------------
#   WISHLIST
# -------------------------

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} wishlist"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.title} in {self.wishlist.user.username} wishlist"

