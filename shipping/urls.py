from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ShippingProviderViewSet, DeliveryViewSet

router = DefaultRouter()
router.register('shipping-providers', ShippingProviderViewSet)
router.register('deliveries', DeliveryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
