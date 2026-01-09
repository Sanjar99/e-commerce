# config/urls.py
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import UserActivateView

schema_view = get_schema_view(
	openapi.Info(
		title = "API E-Commerce",
		default_version = "v1",
		description = "E-commerce API",
		terms_of_service = "https://www.google.com/policies/terms/",
		contact = openapi.Contact(email = "sanjarruzmanov999@gmail.com"),
		license = openapi.License(name = "BSD License"),
	),
   public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (faqat Djoser)
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),

    # ADMIN USER MANAGEMENT
    path('api/v1/admin/', include('accounts.urls')),

    # Other apps
    # path('api/v1/', include("products.urls")),
    # path('api/v1/', include("orders.urls")),
    # path('api/v1/', include("cart.urls")),
    # path('api/v1/', include("payments.urls")),
    # path('api/v1/', include("wishlist.urls")),
    # path('api/v1/', include("reviews.urls")),
    # path('api/v1/', include("coupon.urls")),
    # path('api/v1/', include("notifications.urls")),
    # path('api/v1/', include("staff.urls")),
    # path('api/v1/', include("seller.urls")),
    # path('api/v1/', include("analytics.urls")),
    # path('api/v1/', include("shipping.urls")),
    # path('api/v1/', include("returns.urls")),
    # path('api/v1/', include("logs.urls")),

    # Swagger
    re_path(r"^swagger(?P<format>\.json|\.yaml)$" , schema_view.without_ui(cache_timeout = 0), name = "schema-json"),
    path('', schema_view.with_ui('swagger', cache_timeout = 0), name= "schema-swagger-ui"),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout = 0), name = 'schema-redoc'),

    # Djoser activation endpoint
    path('api/v1/auth/users/activate/<uid>/<token>/', UserActivateView.as_view(), name='user-activate'), # frontend uchun aslida keraksiz

]

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
