from decimal import Decimal

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .factories import CustomerFactory, TransactionFactory
from src.models import Transaction

client = APIClient()


def test_post_transaction_success(transaction_payload):
    url = reverse("transactions-list")
    response = client.post(url, transaction_payload)

    transaction = Transaction.objects.get(reference=transaction_payload["reference"])
    expected_result = transaction_payload
    expected_result["id"] = str(transaction.id)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_result
    assert Transaction.objects.count() == 1


def test_post_transaction_invalid_email(transaction_payload):
    payload = transaction_payload
    payload["user_email"] = "invalid-email"
    url = reverse("transactions-list")

    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"user_email": ["Invalid e-mail format"]}
    assert Transaction.objects.exists() is False


def test_put_transaction_success(transaction_payload):
    transaction = TransactionFactory.create()

    payload = transaction_payload
    payload["id"] = str(transaction.id)
    url = reverse("transactions-detail", args=[transaction.id])

    response = client.put(url, payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == payload

    transaction.refresh_from_db()
    assert transaction.reference == payload["reference"]
    assert transaction.date.isoformat() == payload["date"]
    assert transaction.amount == Decimal(payload["amount"])
    assert transaction.kind == payload["type"]
    assert transaction.user.email == payload["user_email"]
    assert transaction.category.name == payload["category"]


def test_put_transaction_invalid_email(transaction_payload):
    transaction = TransactionFactory.create()

    payload = transaction_payload
    payload["id"] = str(transaction.id)
    payload["user_email"] = "invalid-email"
    url = reverse("transactions-detail", args=[transaction.id])

    response = client.put(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"user_email": ["Invalid e-mail format"]}


def test_patch_transaction_success():
    transaction = TransactionFactory.create()

    payload = {
        "reference": "99995",
        "amount": Decimal("-12345.00"),
        "type": Transaction.Type.OUTFLOW,
        "user_email": "another@email.com",
        "category": "another-category",
    }

    url = reverse("transactions-detail", args=[transaction.id])

    response = client.patch(url, payload)
    assert response.status_code == status.HTTP_200_OK

    transaction.refresh_from_db()
    assert transaction.reference == payload["reference"]
    assert transaction.kind == payload["type"]
    assert transaction.user.email == payload["user_email"]
    assert transaction.category.name == payload["category"]
    assert transaction.amount == payload["amount"]


def test_delete_transaction():
    transaction = TransactionFactory.create()

    url = reverse("transactions-detail", args=[transaction.id])

    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Transaction.objects.exists() is False


def test_get_transaction_success():
    transaction = TransactionFactory.create()
    url = reverse("transactions-detail", args=[transaction.id])

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_list_transactions_success():
    TransactionFactory.create()
    url = reverse("transactions-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_calculate_total_flow_by_users_transactions():
    customer1 = CustomerFactory.create(email="dev1@test.com")
    customer2 = CustomerFactory.create(email="dev2@test.com")

    TransactionFactory.create(
        reference="000100",
        kind=Transaction.Type.INFLOW,
        amount="100.00",
        user_id=customer1.id,
    )
    TransactionFactory.create(
        reference="000200",
        kind=Transaction.Type.OUTFLOW,
        amount="-100.00",
        user_id=customer1.id,
    )
    TransactionFactory.create(
        reference="000300",
        kind=Transaction.Type.OUTFLOW,
        amount="-1000.00",
        user_id=customer2.id,
    )
    url = reverse("transactions-list") + "total/"

    expected_result = [
        {
            "total_inflow": 100.0,
            "total_outflow": -100.0,
            "user_email": "dev1@test.com",
        },
        {
            "total_inflow": 0.0,
            "total_outflow": -1000.0,
            "user_email": "dev2@test.com",
        },
    ]

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_result
