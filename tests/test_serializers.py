import pytest
from rest_framework import serializers

from .factories import CategoryFactory, CustomerFactory, TransactionFactory
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
    assert serializer.is_valid() is True
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

    serializer = TransactionSerializer(data=payload)

    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)
    assert "user_email" in serializer.errors.keys()


def test_validate_transaction_type(transaction_payload):
    payload = transaction_payload
    payload["type"] = "asd"

    serializer = TransactionSerializer(data=payload)
    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)
    assert "type" in serializer.errors.keys()


def test_validate_transaction_reference_if_already_exists(transaction_payload, caplog):
    ref = transaction_payload["reference"]
    TransactionFactory.create(reference=ref)
    payload = transaction_payload
    serializer = TransactionSerializer(data=payload)
    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)
    assert "reference" in serializer.errors.keys()

    log_message = f"Reference={ref} already exists."
    assert log_message in caplog.messages


def test_bulk_create_serializer_if_transaction_already_exists():
    transaction = TransactionFactory.create(
        type=Transaction.INFLOW,
        reference="001",
        amount="9.99",
    )

    test_data = {
        "payload": [
            {
                "reference": "001",
                "date": "2022-03-09",
                "amount": "-100.00",
                "type": "outflow",
                "user_email": "dev1@email.com",
                "category": "category_name",
            },
        ]
    }
    serializer = TransactionBulkCreateSerializer(data=test_data)
    assert serializer.is_valid() is True
    serializer.save()

    assert str(transaction.amount) == "9.99"
    assert transaction.type == Transaction.INFLOW


@pytest.mark.parametrize(
    "transaction_type, transaction_amount, expected_log_value",
    [
        ("inflow", "-100.00", "positive"),
        ("outflow", "100.00", "negative"),
    ],
)
def test_transaction_bulk_create_serializer_with_invalid_transaction_amount(
    transaction_type,
    transaction_amount,
    expected_log_value,
    transaction_payload,
    caplog,
):
    test_data = {
        "payload": [
            transaction_payload,
        ],
    }
    test_data["payload"][0]["type"] = transaction_type
    test_data["payload"][0]["amount"] = transaction_amount

    serializer = TransactionBulkCreateSerializer(data=test_data)

    with pytest.raises(serializers.ValidationError):
        serializer.is_valid(raise_exception=True)

    ref = test_data["payload"][0]["reference"]
    expected_log = f"The transaction amount from reference={ref} must be {expected_log_value}."
    assert expected_log in caplog.messages
