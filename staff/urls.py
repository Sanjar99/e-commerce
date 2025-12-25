from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StaffRoleViewSet,
    StaffUserViewSet,
    ModerationLogViewSet,
    SupportTicketViewSet
)

router = DefaultRouter()
router.register(r'staff-roles', StaffRoleViewSet, basename='staffrole')
router.register(r'staff-users', StaffUserViewSet, basename='staffuser')
router.register(r'moderation-logs', ModerationLogViewSet, basename='moderationlog')
router.register(r'support-tickets', SupportTicketViewSet, basename='supportticket')

# ------------------------------
# URL patterns
# ------------------------------
urlpatterns = [
    path('', include(router.urls)),
]
