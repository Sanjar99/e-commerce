from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StaffRoleViewSet, StaffUserViewSet, ModerationLogViewSet

router = DefaultRouter()
router.register('staff-roles', StaffRoleViewSet)
router.register('staff-users', StaffUserViewSet)
router.register('moderation-logs', ModerationLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
