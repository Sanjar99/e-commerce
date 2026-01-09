from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'phone',
        'is_seller',
        'is_staff',
        'is_active',
        'date_joined',
        'avatar_preview',  # avatar kichik preview
    )

    list_filter = ('is_seller', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone')
    ordering = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ("Qo'shimcha ma'lumotlar", {
            'fields': ('phone', 'avatar', 'is_seller')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Qo'shimcha ma'lumotlar", {
            'fields': ('phone', 'avatar', 'is_seller')
        }),
    )

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="30" height="30" style="border-radius:50%;" />',
                obj.avatar.url
            )
        return "-"
    avatar_preview.short_description = 'Avatar'
