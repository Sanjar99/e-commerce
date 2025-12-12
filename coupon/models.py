from django.db import models

# -------------------------
#   COUPON
# -------------------------

class Coupon(models.Model):
    PERCENT = 'Percent'
    FIXED = 'Fixed Amount'

    DISCOUNT_TYPE_CHOICES = [
        (PERCENT, 'Percent'),
        (FIXED, 'Fixed Amount')
    ]
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    expires_at = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code
