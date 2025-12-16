from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    StaffRoleViewSet,
    StaffUserViewSet,
    ModerationLogViewSet
)

router = DefaultRouter()
router.register('staff-roles', StaffRoleViewSet, basename='staff-role')
router.register('staff-users', StaffUserViewSet, basename='staff-user')
router.register('moderation-logs', ModerationLogViewSet, basename='moderation-log')

urlpatterns = [
    path('', include(router.urls)),
]
