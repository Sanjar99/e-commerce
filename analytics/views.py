from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import RecentlyViewed
from .serializers import RecentlyViewedSerializer

class RecentlyViewedViewSet(viewsets.ModelViewSet):
    serializer_class = RecentlyViewedSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['viewed_at']

    def get_queryset(self):
        return RecentlyViewed.objects.filter(user=self.request.user).order_by('-viewed_at')
