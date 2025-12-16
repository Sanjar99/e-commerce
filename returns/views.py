from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import ReturnRequest
from .serializers import ReturnRequestSerializer

class ReturnRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ReturnRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['status', 'created_at']

    def get_queryset(self):
        user = self.request.user
        return ReturnRequest.objects.filter(user=user)
