from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ReturnRequestViewSet

router = DefaultRouter()
router.register('return-requests', ReturnRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
