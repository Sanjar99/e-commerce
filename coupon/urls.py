from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CouponViewSet

router = DefaultRouter()
router.register('coupons', CouponViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
