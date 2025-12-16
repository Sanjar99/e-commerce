from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser
from seller.models import Seller, SellerBalance, SellerPayout, SellerVerification
from .serializers import  SellerSerializer, SellerBalanceSerializer, SellerPayoutSerializer, SellerVerificationSerializer

# Seller viewset
class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.select_related('user').all()
    serializer_class = SellerSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['shop_name', 'user__username']
    ordering_fields = ['rating', 'created_at']

# Seller Balance
class SellerBalanceViewSet(viewsets.ModelViewSet):
    queryset = SellerBalance.objects.select_related('seller').all()
    serializer_class = SellerBalanceSerializer
    permission_classes = [IsAdminUser]

# Seller Payout
class SellerPayoutViewSet(viewsets.ModelViewSet):
    queryset = SellerPayout.objects.select_related('seller', 'staff').all()
    serializer_class = SellerPayoutSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['amount', 'status', 'requested_at', 'processed_at']

# Seller Verification
class SellerVerificationViewSet(viewsets.ModelViewSet):
    queryset = SellerVerification.objects.select_related('seller', 'staff').all()
    serializer_class = SellerVerificationSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['status', 'created_at', 'updated_at']
