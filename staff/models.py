from django.db import models
from django.contrib.auth.models import User

# -------------------------
# StaffRole
#       Vazifasi: Platformadagi admin/staff rollarini belgilaydi.
#       Nima uchun kerak: Kim nima ish qila olishini ajratish (permission logic).
# -------------------------
class StaffRole(models.Model):
    # Asosiy rollar
    SUPER_ADMIN = 'super_admin'
    CATEGORY_MANAGER = 'category_manager'
    PRODUCT_MODERATOR = 'product_moderator'
    ORDER_MANAGER = 'order_manager'
    FINANCE_MANAGER = 'finance_manager'
    SUPPORT_AGENT = 'support_agent'
    LOGISTICS_AGENT = 'logistics_agent'
    STAFF = 'staff'  # General / Junior Staff

    ROLE_CHOICES = [
        (SUPER_ADMIN, 'Super Admin'),
        (CATEGORY_MANAGER, 'Category Manager'),
        (PRODUCT_MODERATOR, 'Product Moderator'),
        (ORDER_MANAGER, 'Order Manager'),
        (FINANCE_MANAGER, 'Finance Manager'),
        (SUPPORT_AGENT, 'Support Agent'),
        (LOGISTICS_AGENT, 'Logistics Agent'),
        (STAFF, 'Staff'),
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.get_name_display()

# -------------------------
# StaffUser
#       Vazifasi: Platforma xodimlarini saqlaydi.
#       Nima uchun kerak: Oddiy Userni staff sifatida ajratish
#           Qaysi rolga ega ekanini va nimani boshqarishini bilish
# -------------------------
class StaffUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(StaffRole, on_delete=models.SET_NULL, null=True)
    assigned_categories = models.ManyToManyField('products.Category', blank=True)
    assigned_sellers = models.ManyToManyField('seller.Seller', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.get_name_display()}"

# -------------------------
# ModerationLog
#       Vazifasi:Staff qilgan har bir muhim harakatni log qilish.
#       Nima uchun kerak: Audit (kim nima qildi?), Security, Xatoni tekshirish (debug)
# -------------------------
class ModerationLog(models.Model):
    # -------------------------
    # Action constants
    # -------------------------
    APPROVE_PRODUCT = 'approve_product'
    REJECT_PRODUCT = 'reject_product'
    BAN_SELLER = 'ban_seller'
    REFUND_ORDER = 'refund_order'
    UPDATE_INVENTORY = 'update_inventory'
    VERIFY_DOCUMENT = 'verify_document'

    ACTION_CHOICES = [
        (APPROVE_PRODUCT, 'Approve Product'),
        (REJECT_PRODUCT, 'Reject Product'),
        (BAN_SELLER, 'Ban Seller'),
        (REFUND_ORDER, 'Refund Order'),
        (UPDATE_INVENTORY, 'Update Inventory'),
        (VERIFY_DOCUMENT, 'Verify Document'),
    ]

    # -------------------------
    # Target constants
    # -------------------------
    PRODUCT = 'product'
    SELLER = 'seller'
    ORDER = 'order'
    REVIEW = 'review'
    DOCUMENT = 'document'

    TARGET_CHOICES = [
        (PRODUCT, 'Product'),
        (SELLER, 'Seller'),
        (ORDER, 'Order'),
        (REVIEW, 'Review'),
        (DOCUMENT, 'Document'),
    ]
    staff = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_type = models.CharField(max_length=50, choices=TARGET_CHOICES)
    target_id = models.PositiveIntegerField()
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff} - {self.action_type}"

# -------------------------
# SupportTicket
#       Vazifasi: User yoki sellerlardan kelgan support murojaatlarini saqlaydi.
#       Nima uchun kerak: Customer support tizimi
#               Order bilan bog‘liq muammolarni kuzatish
# -------------------------
class SupportTicket(models.Model):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    CLOSED = 'Closed'

    STATUS_CHOICES = [
        (OPEN, 'Open'),
        (IN_PROGRESS, 'In Progress'),
        (CLOSED, 'Closed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey('seller.Seller', on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.PositiveIntegerField(null=True, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=OPEN)
    assigned_staff = models.ForeignKey(StaffUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.status}"