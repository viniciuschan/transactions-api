import itertools
from operator import itemgetter

from django.db.models import Case, F, Q, Sum, Value, When
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customer, Transaction
from .serializers import TransactionBulkCreateSerializer, TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=["post"], url_path="bulk")
    def bulk_create_transactions(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response(
                {"invalid_data": "this endpoint only accepts a list of transactions"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {"payload": request.data}
        serializer = TransactionBulkCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="group-by-user")
    def calculate_total_flow_by_user(self, request, *args, **kwargs):
        data = (
            Transaction.objects.values(user_email=F("user__email"))
            .annotate(
                total_inflow=Sum(
                    F("amount"),
                    filter=Q(kind=Transaction.Type.INFLOW),
                    default=0,
                ),
            )
            .annotate(
                total_outflow=Sum(
                    F("amount"),
                    filter=Q(kind=Transaction.Type.OUTFLOW),
                    default=0,
                ),
            )
        )

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="summary")
    def get_summary_transactions_by_email(self, request, *args, **kwargs):
        user_email = request.query_params.get("user_email")
        customer = get_object_or_404(Customer, email=user_email)

        transactions = (
            Transaction.objects.filter(user=customer)
            .select_related("category")
            .values("amount", category_name=F("category__name"))
            .annotate(
                kind=Case(
                    When(kind=Transaction.Type.INFLOW, then=Value("inflow")),
                    When(kind=Transaction.Type.OUTFLOW, then=Value("outflow")),
                )
            )
        )

        data = {}
        for key, group in itertools.groupby(transactions, key=itemgetter("kind")):
            categories = list(group)
            data[key] = {item["category_name"]: str(item["amount"]) for item in categories}

        return Response(data, status.HTTP_200_OK)
