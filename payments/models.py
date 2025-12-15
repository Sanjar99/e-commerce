from django.db import models

from orders.models import Order

# -------------------------
# Payment
#       Vazifasi:  Buyurtmaning to‘lov holatini saqlaydi.
#       Nima uchun kerak:Order uchun to‘lov qilinganmi yoki yo‘qmi – shuni boshqarish uchun.
#           Payment gateway (Click, Payme, Stripe va h.k.) bilan integratsiyada real to‘lov ma’lumotlarini saqlash uchun.
# -------------------------

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment for {self.order.order_number}"
