from django.db import models
from django.contrib.auth.models import User

from products.models import SellerProduct

# -------------------------
# Cart
#       Vazifasi:Foydalanuvchining savatini (shopping cart) saqlaydi.
#       Nima uchun kerak: Har bir user uchun alohida cart yaratish va buyurtma qilinmaguncha productlarni saqlash uchun.
#       Qiziq nuqta:created_at orqali cartning qachon yaratilganini kuzatish mumkin.
# -------------------------
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

# -------------------------
# CartItem
#       Vazifasi:Savatdagi har bir itemni saqlaydi (qaysi sellerning producti, miqdori va narxi).
#       Nima uchun kerak:  Savatdagi productlar, quantity va o‘sha paytdagi narxni saqlash uchun.
#       Qiziq nuqta:price_at_that_moment orqali narx keyinchalik o‘zgarsa ham, cartdagi narx o‘sha vaqtdagi qiymat bo‘lib qoladi.
# -------------------------
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_that_moment = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.seller_product} x{self.quantity}"