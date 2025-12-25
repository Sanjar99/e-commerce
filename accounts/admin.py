from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_seller', 'is_staff_user', 'is_staff', 'is_active')
    list_filter = ('is_seller', 'is_staff_user', 'is_staff', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ("Qo'shimcha ma'lumotlar", {
            'fields': ('phone', 'avatar', 'is_seller', 'is_staff_user')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Qo'shimcha ma'lumotlar", {
            'fields': ('phone', 'avatar', 'is_seller', 'is_staff_user')
        }),
    )