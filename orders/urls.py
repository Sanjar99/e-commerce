from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    OrderViewSet,
    OrderSellerGroupViewSet,
    OrderItemViewSet
)

router = DefaultRouter()
router.register('orders', OrderViewSet)
router.register('order-groups', OrderSellerGroupViewSet)
router.register('order-items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
