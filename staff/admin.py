from django.contrib import admin
from .models import StaffRole, StaffUser, ModerationLog, SupportTicket

# ------------------------------
# StaffRole admin
# ------------------------------
@admin.register(StaffRole)
class StaffRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name', 'description')
    ordering = ('id',)


# ------------------------------
# StaffUser admin
# ------------------------------
@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'assigned_categories', 'assigned_sellers')
    search_fields = ('user__username', 'user__email', 'role__name')
    ordering = ('-created_at',)
    filter_horizontal = ('assigned_categories', 'assigned_sellers')


# ------------------------------
# ModerationLog admin
# ------------------------------
@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'action_type', 'target_type', 'target_id', 'created_at')
    list_filter = ('action_type', 'target_type', 'staff__role')
    search_fields = ('staff__user__username', 'note')
    ordering = ('-created_at',)


# ------------------------------
# SupportTicket admin
# ------------------------------
@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'status', 'user', 'assigned_staff', 'created_at')
    list_filter = ('status', 'assigned_staff', 'seller')
    search_fields = ('subject', 'message', 'user__username', 'seller__shop_name')
    ordering = ('-created_at',)
