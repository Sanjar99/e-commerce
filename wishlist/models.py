from django.db import models
from django.conf import settings
from products.models import Product

# -------------------------
# Wishlist
#       Vazifasi:Foydalanuvchi yoqtirgan yoki keyinroq sotib olmoqchi bo‘lgan productlar ro‘yxatini saqlaydi.
#       Nima uchun kerak: User experience’ni yaxshilash
#               “Save for later” funksiyasi
#               Marketing (wishlist’dagi productlar bo‘yicha promo)
# -------------------------
class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} wishlist"
# -------------------------
# WishlistItem
#       Vazifasi: Wishlist ichidagi har bir productni alohida saqlaydi.
#       Nima uchun kerak: Bitta wishlist’da ko‘p product bo‘lishi uchun
#               Productni wishlist’ga qo‘shish / olib tashlashni oson qilish uchun
# -------------------------
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.title} in {self.wishlist.user.username} wishlist"

