from django.db import models
from django.contrib.auth.models import User

from products.models import Product

# -------------------------
#   Review
#       Vazifasi: Foydalanuvchi tomonidan productga berilgan sharh va reytinglarni saqlaydi.
#       Nima uchun kerak:Foydalanuvchilar product sifatini baholashlari uchun.
#           Marketplace’da product reytingini hisoblash va ko‘rsatish uchun (average rating).
#       Qiziq nuqta:related_name='reviews' orqali product.reviews.all() orqali shu productga berilgan barcha sharhlarni olish mumkin.
#           rating 1–5 yoki boshqa oraliqda bo‘lishi mumkin, UI’da yulduzcha ko‘rinishida chiqadi.
# -------------------------
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"