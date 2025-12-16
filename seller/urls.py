from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    SellerViewSet,
    SellerBalanceViewSet,
    SellerPayoutViewSet,
    SellerVerificationViewSet
)

router = DefaultRouter()
router.register('sellers', SellerViewSet, basename='seller')
router.register('seller-balances', SellerBalanceViewSet, basename='seller-balance')
router.register('seller-payouts', SellerPayoutViewSet, basename='seller-payout')
router.register('seller-verifications', SellerVerificationViewSet, basename='seller-verification')

urlpatterns = [
    path('', include(router.urls)),
]
