from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
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
