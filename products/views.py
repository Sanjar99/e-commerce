# products/views.py
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from services.permissions import IsAdminOrStaff
from .models import (
    Category, Brand, Product, ProductImage,
    ProductOption, ProductOptionValue,
    ProductVariant, SellerProduct,
    SellerVariantOffer, Inventory,
    ProductModeration
)
from .serializers import (
    CategoryTreeSerializer, CategorySerializer,
    BrandSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer,
    ProductImageSerializer,
    ProductOptionSerializer, ProductOptionValueSerializer,
    ProductVariantReadSerializer, ProductVariantWriteSerializer,
    SellerProductSerializer,
    SellerVariantOfferReadSerializer, SellerVariantOfferWriteSerializer,
    ProductModerationSerializer,
)


# -------------------------
# PUBLIC: Categories
# -------------------------
class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.filter(is_active=True).select_related("parent")
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    @action(detail=False, methods=["get"], url_path="tree")
    def tree(self, request):
        roots = Category.objects.filter(is_active=True, parent__isnull=True).order_by("ordering", "name")
        data = CategoryTreeSerializer(roots, many=True).data
        return Response(data)


# -------------------------
# PUBLIC: Brands
# -------------------------
class BrandViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"


# -------------------------
# PUBLIC: Products (List/Detail)
# -------------------------
class ProductPublicViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    lookup_field = "slug"

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "rating_avg", "rating_count"]
    ordering = ["-created_at"]

    # basic filters (category, brand, status)
    filterset_fields = ["category", "brand"]

    def get_queryset(self):
        qs = (
            Product.objects
            .filter(status=Product.Status.ACTIVE)
            .select_related("category", "brand")
            .prefetch_related("images")
            .prefetch_related("options__values")
            .prefetch_related("variants__selections__option", "variants__selections__value")
        )
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer


# -------------------------
# DASHBOARD: Products CRUD (Admin/Staff yoki Seller)
# -------------------------
class ProductDashboardViewSet(viewsets.ModelViewSet):
    """
    Dashboard orqali catalog product yaratish.
    Amazon’da odatda admin/staff yaratadi, seller offer qo‘shadi.
    Sen xohlasang sellerga ham ruxsat beramiz.
    """
    queryset = Product.objects.all().select_related("category", "brand").prefetch_related("images")
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # hozircha admin/staff

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    filterset_fields = ["status", "category", "brand"]

    @action(detail=True, methods=["post"], url_path="images")
    def add_image(self, request, pk=None):
        product = self.get_object()
        serializer = ProductImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -------------------------
# DASHBOARD: Options + Values
# -------------------------
class ProductOptionViewSet(viewsets.ModelViewSet):
    queryset = ProductOption.objects.all().select_related("product")
    serializer_class = ProductOptionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product"]


class ProductOptionValueViewSet(viewsets.ModelViewSet):
    queryset = ProductOptionValue.objects.all().select_related("option", "option__product")
    serializer_class = ProductOptionValueSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["option"]


# -------------------------
# DASHBOARD: SKU Variants
# -------------------------
class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all().select_related("product").prefetch_related(
        "selections__option", "selections__value"
    )
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["sku"]
    filterset_fields = ["product", "is_active"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ProductVariantWriteSerializer
        return ProductVariantReadSerializer


# -------------------------
# DASHBOARD: Seller offers (SellerProduct)
# -------------------------
class SellerProductViewSet(viewsets.ModelViewSet):
    queryset = SellerProduct.objects.all().select_related("seller", "product")
    serializer_class = SellerProductSerializer
    permission_classes = [IsAuthenticated]  # seller login bo'lishi kerak

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["product__title", "product__slug"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    filterset_fields = ["seller", "product", "is_active"]

    def perform_create(self, serializer):
        """
        Seller o'zi uchun offer yaratadi:
        request.user -> seller mapping bo‘lishi kerak.
        Agar sende Seller modeli userga bog'langan bo'lsa, shu yerda olish mumkin.
        """
        # Agar Seller modelda user FK bo'lsa:
        # seller = self.request.user.seller
        # serializer.save(seller=seller)

        serializer.save()


# -------------------------
# DASHBOARD: Seller price per SKU + inventory
# -------------------------
class SellerVariantOfferViewSet(viewsets.ModelViewSet):
    queryset = SellerVariantOffer.objects.all().select_related(
        "seller_product", "variant", "seller_product__product"
    ).prefetch_related("variant__selections__option", "variant__selections__value")

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["variant__sku", "seller_product__product__title"]
    ordering_fields = ["created_at", "updated_at", "price"]
    ordering = ["-created_at"]
    filterset_fields = ["seller_product", "variant", "is_active"]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return SellerVariantOfferWriteSerializer
        return SellerVariantOfferReadSerializer


# -------------------------
# DASHBOARD: Moderation (staff approves seller listing)
# -------------------------
class ProductModerationViewSet(viewsets.ModelViewSet):
    queryset = ProductModeration.objects.all().select_related("seller_product", "staff")
    serializer_class = ProductModerationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "seller_product"]
