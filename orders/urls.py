from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    OrderViewSet,
    OrderSellerGroupViewSet,
    OrderItemViewSet
)

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')
router.register('order-groups', OrderSellerGroupViewSet, basename='order-group')
router.register('order-items', OrderItemViewSet, basename='order-item')

urlpatterns = [
    path('', include(router.urls)),
]
