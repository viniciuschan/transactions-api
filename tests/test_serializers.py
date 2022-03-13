import pytest
from rest_framework import serializers

from .factories import CategoryFactory, CustomerFactory
from src.models import Category, Customer, Transaction
from src.serializers import (
    TransactionBulkCreateSerializer,
    TransactionSerializer,
    get_category_id,
    get_user_id,
)


@pytest.mark.parametrize(
    "user_email, users_count",
    [
        ({"email": "dev@test.com"}, 1),
        ({"email": "another-email@test.com"}, 2),
    ],
    ids=[
        "should_not_create_another_user",
        "should_create_new_user",
    ],
)
def test_get_user_id(user_email, users_count):
    CustomerFactory.create(email="dev@test.com")

    get_user_id(user_email)
    assert Customer.objects.count() == users_count


@pytest.mark.parametrize(
    "category_name, categories_count",
    [
        ({"name": "finances"}, 1),
        ({"name": "another-category"}, 2),
    ],
    ids=[
        "should_not_create_another_user",
        "should_create_new_user",
    ],
)
def test_get_category_id(category_name, categories_count):
    CategoryFactory.create(name="finances")

    get_category_id(category_name)
    assert Category.objects.count() == categories_count


def test_transaction_serializer_success(transaction_payload):
    serializer = TransactionSerializer(data=transaction_payload)
    serializer.is_valid() is True
    serializer.save()

    transaction = Transaction.objects.get(reference=transaction_payload["reference"])
    assert transaction.reference == transaction_payload["reference"]
    assert transaction.type == transaction_payload["type"]
    assert transaction.user.email == transaction_payload["user_email"]
    assert transaction.category.name == transaction_payload["category"]
    assert str(transaction.amount) == transaction_payload["amount"]


def test_transaction_serializer_invalid_email(transaction_payload):
    payload = transaction_payload
    payload["user_email"] = "invalid-email"

    serializer = TransactionSerializer(data=transaction_payload)

    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)
    assert "user_email" in serializer.errors.keys()


def test_validate_transaction_type(transaction_payload):
    payload = transaction_payload
    payload["type"] = "asd"

    serializer = TransactionSerializer(data=transaction_payload)

    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)
    assert "type" in serializer.errors.keys()


@pytest.mark.parametrize(
    "transaction_type, transaction_amount",
    [
        ("inflow", "-100.00"),
        ("outflow", "100.00"),
    ],
)
def test_transaction_serializer_invalid_transaction_amount(
    transaction_type,
    transaction_amount,
    transaction_payload,
):
    data = {
        "payload": [
            transaction_payload,
        ],
    }
    data["payload"][0]["type"] = transaction_type
    data["payload"][0]["amount"] = transaction_amount

    serializer = TransactionBulkCreateSerializer(data=data)

    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)
