# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

urlpatterns = [
    path('', lambda request: JsonResponse({"status": "API is running"})),

    path('admin/', admin.site.urls),

    # Accounts / Authentication
    path('api/accounts/', include('accounts.urls')),

    # Products
    path('api/products/', include('products.urls')),

    # Orders
    path('api/orders/', include('orders.urls')),

    # Cart
    path('api/cart/', include('cart.urls')),

    # Payments
    path('api/payments/', include('payments.urls')),

    # Wishlist
    path('api/wishlist/', include('wishlist.urls')),

    # Reviews
    path('api/reviews/', include('reviews.urls')),

    # Coupon / Discounts
    path('api/coupons/', include('coupon.urls')),

    # Notifications
    path('api/notifications/', include('notifications.urls')),

    # Staff / Admin
    path('api/staff/', include('staff.urls')),

    # Seller
    path('api/seller/', include('seller.urls')),

    # Analytics
    path('api/analytics/', include('analytics.urls')),

    # Shipping / Delivery
    path('api/shipping/', include('shipping.urls')),

    # Returns / Refunds
    path('api/returns/', include('returns.urls')),

    # Logs / Activity
    path('api/logs/', include('logs.urls')),
]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
