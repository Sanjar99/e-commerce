from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    SellerViewSet,
    SellerBalanceViewSet,
    SellerPayoutViewSet,
    SellerVerificationViewSet
)

router = DefaultRouter()
router.register('sellers', SellerViewSet)
router.register('seller-balances', SellerBalanceViewSet)
router.register('seller-payouts', SellerPayoutViewSet)
router.register('seller-verifications', SellerVerificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
