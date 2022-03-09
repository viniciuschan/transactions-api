import pytest
from rest_framework import serializers

from src.models import Category, Customer, Transaction
from src.serializers import TransactionSerializer

pytestmark = pytest.mark.django_db


def test_transaction_serializer_success(transaction_payload):
    Transaction.objects.count() == 0
    Category.objects.count() == 0
    Customer.objects.count() == 0

    serializer = TransactionSerializer(data=transaction_payload)
    serializer.is_valid(raise_exception=True) is True
    serializer.save()

    Transaction.objects.count() == 1
    Category.objects.count() == 1
    Customer.objects.count() == 1


def test_transaction_serializer_invalid_email(transaction_payload):
    payload = transaction_payload
    payload["user_email"] = "invalid-email"

    serializer = TransactionSerializer(data=transaction_payload)

    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)

    Category.objects.count() == 0
    Customer.objects.count() == 0
    Transaction.objects.count() == 0
