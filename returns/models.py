from django.db import models
from order.models import OrderItem
from django.contrib.auth.models import User

from staff.models import StaffUser

# -------------------------
# ReturnRequest
#       Vazifasi: Foydalanuvchining mahsulotni qaytarish (refund/return) so‘rovini saqlaydi.
#       Nima uchun kerak: Order ichidagi bitta product (OrderItem) bo‘yicha qaytarish jarayonini boshqarish uchun.
#               Admin/Staff tomonidan tekshirilib, tasdiqlash yoki rad etish uchun.
# -------------------------
class ReturnRequest(models.Model):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    REFUNDED = 'Refunded'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (REFUNDED, 'Refunded'),
    ]
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    staff = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
