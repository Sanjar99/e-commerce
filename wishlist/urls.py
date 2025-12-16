from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import WishlistViewSet, WishlistItemViewSet

router = DefaultRouter()
router.register('wishlists', WishlistViewSet)
router.register('wishlist-items', WishlistItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
