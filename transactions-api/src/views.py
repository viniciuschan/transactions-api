from django.db.models import F, Q, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=["get"], url_path="total")
    def calculate_total_flow_by_user(self, request, *args, **kwargs):
        data = (
            Transaction.objects.values(user_email=F("user__email"))
            .annotate(
                total_inflow=Sum(F("amount"), filter=Q(kind="IN")),
            )
            .annotate(
                total_outflow=Sum(F("amount"), filter=Q(kind="OU")),
            )
        )

        return Response(data, status=status.HTTP_200_OK)
