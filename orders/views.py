from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderItem, OrderSellerGroup

from .serializers import OrderSerializer, OrderItemSerializer, OrderSellerGroupSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'total_price']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(seller_group__order__user=self.request.user)


class OrderSellerGroupViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSellerGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderSellerGroup.objects.filter(order__user=self.request.user)


