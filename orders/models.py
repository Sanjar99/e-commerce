from django.db import models
from django.contrib.auth.models import User

from products.models import SellerProduct
from seller.models import Seller


# -------------------------
# Address
#       Vazifasi: Foydalanuvchining yetkazib berish manzillarini saqlaydi.
#       Nima uchun kerak: Har bir user bir yoki bir nechta manzilga ega bo‘lishi mumkin; is_default orqali asosiy manzilni belgilash mumkin.
# -------------------------
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.street}"


# -------------------------
# Order
#       Vazifasi: Foydalanuvchi tomonidan berilgan buyurtmani saqlaydi.
#       Nima uchun kerak:Orderning umumiy ma’lumotlarini (total_price, total_items, status, payment_method) boshqarish uchun.
#       Qiziq nuqta: Har order bir nechta sellerni o‘z ichiga olishi mumkin → distributsiya uchun OrderSellerGroup.
# -------------------------
class Order(models.Model):
    PENDING = "Pending"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    COMPLETED = "Completed"
    CANCELED = "Canceled"

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, unique=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_items = models.PositiveIntegerField(default=0)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=PENDING)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - order number - {self.order_number}"


# -------------------------
# OrderSellerGroup
#       Vazifasi: Har orderdagi har bir seller uchun alohida guruh yaratadi.
#       Nima uchun kerak: Marketplace’da 1 order ichida bir nechta seller bo‘lishi mumkin; har seller uchun shipment va statusni alohida kuzatish uchun.
# -------------------------
class OrderSellerGroup(models.Model):
    AWAITING = 'Awaiting'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    
    STATUS_CHOICES = [
        (AWAITING, 'Awaiting'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='seller_groups')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    seller_total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AWAITING)

    def __str__(self):
        return f"{self.order.order_number} - {self.seller.shop_name}"
# -------------------------
# OrderItem
#       Vazifasi: OrderSellerGroup’dagi har bir productni saqlaydi.
#       Nima uchun kerak: Qaysi sellerdan qaysi product buyurtma qilinganini, quantity va price bilan saqlash uchun.
#       Qiziq nuqta: seller_group orqali har sellerning buyurtma items’ini ajratib olish mumkin.
# -------------------------
class OrderItem(models.Model):
    seller_group = models.ForeignKey(OrderSellerGroup, on_delete=models.CASCADE, related_name='items')
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.seller_product} x {self.quantity}"
    

