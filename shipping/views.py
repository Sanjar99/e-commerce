from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from .models import ShippingProvider, Delivery
from .serializers import ShippingProviderSerializer, DeliverySerializer

class ShippingProviderViewSet(viewsets.ModelViewSet):
    queryset = ShippingProvider.objects.all()
    serializer_class = ShippingProviderSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id', 'name']

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.select_related('ordersellergroup', 'provider').all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['status', 'updated_at']
