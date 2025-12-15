from django.db import models
from django.contrib.auth.models import User
from staff.models import StaffUser

# -------------------------
# ShippingProvider
#       Vazifasi: Tizimda bo‘layotgan muhim harakatlarni log qilish (audit trail).
#       Nima uchun kerak: Security (kim nima qildi?)
#               Debugging (qachon va nima o‘zgardi?)
#               Audit (admin/staff faoliyatini tekshirish)
# -------------------------
class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    staff = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    meta_json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.created_at}"
