# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminUserViewSet,
    UserMeView,
    UpdateProfileView,
    UserActivateView
)
from djoser import views as djoser_views

router = DefaultRouter()
router.register('users', AdminUserViewSet, basename='user')  # SuperAdmin CRUD

urlpatterns = [
    # Router orqali SuperAdmin /users/ endpoint
    path('', include(router.urls)),

    # Oddiy user profile endpointlari
    path('me/', UserMeView.as_view(), name='user-me'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),

    # User activation
    path('auth/users/activate/<uid>/<token>/', UserActivateView.as_view(), name='user-activate'),
]
