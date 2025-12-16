from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import SupportTicket
from .serializers import SupportTicketSerializer

class SupportTicketViewSet(viewsets.ModelViewSet):
    serializer_class = SupportTicketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['subject', 'message']
    ordering_fields = ['status', 'created_at']

    def get_queryset(self):
        user = self.request.user
        # Foydalanuvchi faqat o'z ticketlarini ko'radi
        return SupportTicket.objects.filter(user=user)
