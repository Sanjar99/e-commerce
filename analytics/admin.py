from django.contrib import admin
from .models import AnalyticsDaily, RecentlyViewed

# -------------------------
# AnalyticsDaily Admin
# -------------------------
@admin.register(AnalyticsDaily)
class AnalyticsDailyAdmin(admin.ModelAdmin):
    list_display = ('date', 'users_count', 'orders_count', 'revenue', 'seller_count', 'new_products')
    list_filter = ('date',)
    readonly_fields = ('date', 'users_count', 'orders_count', 'revenue', 'seller_count', 'new_products')
    ordering = ('-date',)
    search_fields = ('date',)


# -------------------------
# RecentlyViewed Admin
# -------------------------
@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('user', 'product', 'viewed_at')
    ordering = ('-viewed_at',)
