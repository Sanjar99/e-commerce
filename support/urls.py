from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SupportTicketViewSet

router = DefaultRouter()
router.register('support-tickets', SupportTicketViewSet, basename='support')

urlpatterns = [
    path('', include(router.urls)),
]
