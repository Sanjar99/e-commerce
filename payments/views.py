from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from payments.models import Payment

from payments.serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)
