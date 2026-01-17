# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdminUserViewSet,
    UserMeView,
    UpdateProfileView,
    UserActivateView,
    CustomUserViewSet
)

router = DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='admin-users')  # admin user management (GET/PATCH)
urlpatterns = [
    # Admin users CRUD
    path('', include(router.urls)),

    # User self endpoints
    path('me/', UserMeView.as_view(), name='user-me'),
    path('me/update/', UpdateProfileView.as_view(), name='user-update'),

    # Activation
    path(
        'auth/activate/<uid>/<token>/',
        UserActivateView.as_view(),
        name='user-activate'
    ),
]
