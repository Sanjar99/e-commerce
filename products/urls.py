# products/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    BrandViewSet,
    ProductPublicViewSet,

    ProductDashboardViewSet,
    ProductOptionViewSet,
    ProductOptionValueViewSet,
    ProductVariantViewSet,
    SellerProductViewSet,
    SellerVariantOfferViewSet,
    ProductModerationViewSet,
)

# =========================
# Routers
# =========================
public_router = DefaultRouter()
dashboard_router = DefaultRouter()

# -------------------------
# PUBLIC (Frontend)
# -------------------------
public_router.register(r'categories', CategoryViewSet, basename='categories')
public_router.register(r'brands', BrandViewSet, basename='brands')
public_router.register(r'products', ProductPublicViewSet, basename='products')

# -------------------------
# DASHBOARD (Admin / Seller)
# -------------------------
dashboard_router.register(r'products', ProductDashboardViewSet, basename='dashboard-products')
dashboard_router.register(r'options', ProductOptionViewSet, basename='product-options')
dashboard_router.register(r'option-values', ProductOptionValueViewSet, basename='product-option-values')
dashboard_router.register(r'variants', ProductVariantViewSet, basename='product-variants')
dashboard_router.register(r'seller-products', SellerProductViewSet, basename='seller-products')
dashboard_router.register(r'variant-offers', SellerVariantOfferViewSet, basename='seller-variant-offers')
dashboard_router.register(r'moderations', ProductModerationViewSet, basename='product-moderations')

urlpatterns = [
    # Public API
    path('', include(public_router.urls)),

    # Dashboard API
    path('dashboard/', include(dashboard_router.urls)),
]
