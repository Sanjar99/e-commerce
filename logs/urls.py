from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ActivityLogViewSet

router = DefaultRouter()

router.register('activity-logs', ActivityLogViewSet, basename='logs')

urlpatterns = [
    path('', include(router.urls)),
]
