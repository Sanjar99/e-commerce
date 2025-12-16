from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RecentlyViewedViewSet

router = DefaultRouter()
router.register('recently-viewed', RecentlyViewedViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
