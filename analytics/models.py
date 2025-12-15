from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# -------------------------
# AnalyticsDaily
#       Vazifasi:Har kunlik marketplace statistikasini saqlaydi.
#       Nima uchun kerak: Admin panelda yoki dashboard’da kunlik analytics ko‘rsatish uchun: foydalanuvchilar soni, buyurtmalar, daromad, yangi sellerlar va mahsulotlar.
#       Qiziq nuqta: Backend avtomatik kunlik hisobotlarni yangilashi mumkin.
# -------------------------
class AnalyticsDaily(models.Model):
    date = models.DateField()
    users_count = models.PositiveIntegerField(default=0)
    orders_count = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    seller_count = models.PositiveIntegerField(default=0)
    new_products = models.PositiveIntegerField(default=0)

# -------------------------
# RecentlyViewed
#       Vazifasi:Foydalanuvchi tomonidan yaqinda ko‘rilgan productlarni saqlaydi.
#       Nima uchun kerak:Shaxsiy tavsiyalar, “recently viewed” bo‘limi yoki marketing uchun.
#       Qiziq nuqta:Har product ko‘rilganda viewed_at saqlanadi, bu orqali eng so‘nggi ko‘rilgan productlarni tartiblash mumkin.
# -------------------------
class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
