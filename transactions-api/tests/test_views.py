import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .factories import TransactionFactory
from src.models import Transaction

pytestmark = pytest.mark.django_db
client = APIClient()


def test_post_transactions_success(transaction_payload):
    url = reverse("transactions-list")
    response = client.post(url, transaction_payload)

    transaction = Transaction.objects.get(reference=transaction_payload["reference"])
    expected_result = transaction_payload
    expected_result["id"] = str(transaction.id)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == expected_result


def test_post_transactions_invalid_email(transaction_payload):
    payload = transaction_payload
    payload["user_email"] = "invalid-email"
    url = reverse("transactions-list")

    response = client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"user_email": ["Invalid e-mail format"]}
    assert Transaction.objects.filter(reference=payload["reference"]).exists() is False


def test_put_transactions_success(transaction_payload):
    transaction = TransactionFactory.create()

    payload = transaction_payload
    payload["id"] = str(transaction.id)
    url = reverse("transactions-detail", args=[transaction.id])

    response = client.put(url, payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == payload
    assert Transaction.objects.count() == 1


def test_put_transactions_invalid_email(transaction_payload):
    transaction = TransactionFactory.create()

    payload = transaction_payload
    payload["id"] = str(transaction.id)
    payload["user_email"] = "invalid-email"
    url = reverse("transactions-detail", args=[transaction.id])

    response = client.put(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"user_email": ["Invalid e-mail format"]}
    assert Transaction.objects.filter(reference=payload["reference"]).exists() is False


def test_patch_transactions_success(transaction_payload):
    transaction = TransactionFactory.create()

    payload = transaction_payload
    payload.pop("date")
    url = reverse("transactions-detail", args=[transaction.id])

    response = client.patch(url, payload)
    assert response.status_code == status.HTTP_200_OK
    assert Transaction.objects.count() == 1


def test_delete_transactions():
    transaction = TransactionFactory.create()

    url = reverse("transactions-detail", args=[transaction.id])

    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Transaction.objects.count() == 0


def test_get_transactions_success():
    transaction = TransactionFactory.create()
    url = reverse("transactions-detail", args=[transaction.id])

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_list_transactions_success():
    TransactionFactory.create()
    url = reverse("transactions-list")

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
