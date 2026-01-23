from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # =========================
    # LIST PAGE
    # =========================
    list_display = (
        'username',
        'email',
        'phone',
        'is_seller',
        'is_staff',
        'is_active',
        'date_joined',
        'avatar_preview',
    )

    list_filter = (
        'is_seller',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'phone',
    )

    ordering = ('-date_joined',)
    list_per_page = 25

    # =========================
    # DETAIL / EDIT PAGE
    # =========================
    readonly_fields = (
        'last_login',
        'date_joined',
        'avatar_preview',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Qo‘shimcha ma’lumotlar",
            {
                'fields': (
                    'phone',
                    'avatar',
                    'avatar_preview',
                    'is_seller',
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Qo‘shimcha ma’lumotlar",
            {
                'fields': (
                    'phone',
                    'avatar',
                    'is_seller',
                )
            },
        ),
    )

    # =========================
    # METHODS
    # =========================
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="36" height="36" '
                'style="border-radius:50%; object-fit:cover;" />',
                obj.avatar.url
            )
        return "—"

    avatar_preview.short_description = "Avatar"
