from decimal import Decimal

from django.db import connection
from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from .factories import CategoryFactory, CustomerFactory, TransactionFactory
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
    assert response.json() == {"user_email": ["Enter a valid email address."]}
    assert Transaction.objects.exists() is False


def test_put_transaction_not_allowed(transaction_payload):
    transaction = TransactionFactory.create()

    payload = transaction_payload
    payload["id"] = str(transaction.id)
    url = reverse("transactions-detail", args=[transaction.id])

    response = client.put(url, payload)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patch_transaction_not_allowed():
    transaction = TransactionFactory.create()

    payload = {
        "reference": "99995",
        "amount": Decimal("-12345.00"),
        "type": Transaction.OUTFLOW,
        "user_email": "another@email.com",
        "category": "another-category",
    }

    url = reverse("transactions-detail", args=[transaction.id])

    response = client.patch(url, payload)
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


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


def test_bulk_create_transactions_success():
    payload = [
        {
            "reference": "0000001",
            "date": "2022-03-09",
            "amount": "100.00",
            "type": "inflow",
            "user_email": "dev1@email.com",
            "category": "category_name",
        },
        {
            "reference": "0000002",
            "date": "2022-03-09",
            "amount": "-100.00",
            "type": "outflow",
            "user_email": "dev2@email.com",
            "category": "another_category_name",
        },
    ]
    url = reverse("transactions-list") + "bulk/"

    response = client.post(url, data=payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED


def test_bulk_create_transactions_with_duplicated_items():
    TransactionFactory.create(
        reference="0000001",
        amount="0.00",
    )
    payload = [
        {
            "reference": "0000001",
            "date": "2022-03-09",
            "amount": "100.00",
            "type": "inflow",
            "user_email": "dev1@email.com",
            "category": "category_name",
        },
        {
            "reference": "0000002",
            "date": "2022-03-09",
            "amount": "-200.00",
            "type": "outflow",
            "user_email": "dev1@email.com",
            "category": "category_name",
        },
        {
            "reference": "0000002",
            "date": "2022-03-09",
            "amount": "300.00",
            "type": "inflow",
            "user_email": "dev2@email.com",
            "category": "another_category_name",
        },
    ]
    url = reverse("transactions-list") + "bulk/"

    response = client.post(url, data=payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    assert Transaction.objects.count() == 2
    transaction1 = Transaction.objects.get(reference=payload[0]["reference"])
    assert transaction1.amount == Decimal("0.00")

    transaction2 = Transaction.objects.get(reference=payload[1]["reference"])
    assert transaction2.amount == Decimal("-200.00")


def test_bulk_create_transactions_with_invalid_format():
    url = reverse("transactions-list") + "bulk/"
    invalid_payload = {"key": "value"}

    expected_result = {"invalid_data": "This endpoint only accepts a list of transactions."}

    response = client.post(url, invalid_payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_result


@override_settings(DEBUG=True)
def test_calculate_total_flow_by_users_transactions():
    customer1 = CustomerFactory.create(email="dev1@test.com")
    customer2 = CustomerFactory.create(email="dev2@test.com")

    TransactionFactory.create(
        reference="000100",
        type=Transaction.INFLOW,
        amount=Decimal("100.00"),
        user_id=customer1.id,
    )
    TransactionFactory.create(
        reference="000200",
        type=Transaction.OUTFLOW,
        amount=Decimal("-100.00"),
        user_id=customer1.id,
    )
    TransactionFactory.create(
        reference="000300",
        type=Transaction.OUTFLOW,
        amount=Decimal("-1000.00"),
        user_id=customer2.id,
    )
    url = reverse("transactions-list") + "group-by-user/"

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

    # optimized query
    assert len(connection.queries) == 1


@override_settings(DEBUG=True)
def test_get_summary_transactions_by_email_success():
    customer = CustomerFactory.create(email="dev@test.com")
    customer2 = CustomerFactory.create(email="dev2@test.com")
    category1 = CategoryFactory.create(name="salary")
    category2 = CategoryFactory.create(name="savings")
    category3 = CategoryFactory.create(name="groceries")
    category4 = CategoryFactory.create(name="rent")
    category5 = CategoryFactory.create(name="transfer")

    TransactionFactory.create(
        reference="000100",
        type=Transaction.INFLOW,
        amount=Decimal("2500.00"),
        user=customer,
        category=category1,
    )
    TransactionFactory.create(
        reference="000200",
        type=Transaction.INFLOW,
        amount=Decimal("150.72"),
        user=customer,
        category=category2,
    )
    TransactionFactory.create(
        reference="000300",
        type=Transaction.OUTFLOW,
        amount=Decimal("-51.13"),
        user=customer,
        category=category3,
    )
    TransactionFactory.create(
        reference="000400",
        type=Transaction.OUTFLOW,
        amount=Decimal("-560.00"),
        user=customer,
        category=category4,
    )
    TransactionFactory.create(
        reference="000500",
        type=Transaction.OUTFLOW,
        amount=Decimal("-150.72"),
        user=customer,
        category=category5,
    )
    TransactionFactory.create(
        reference="000600",
        type=Transaction.INFLOW,
        amount=Decimal("100000.72"),
        user=customer2,
        category=category5,
    )

    expected_result = {
        "inflow": {
            "salary": "2500.00",
            "savings": "150.72",
        },
        "outflow": {
            "groceries": "-51.13",
            "rent": "-560.00",
            "transfer": "-150.72",
        },
    }
    url = reverse("transactions-list") + "summary/?user_email=dev@test.com"

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected_result

    # optimized query
    assert len(connection.queries) == 2


def test_get_summary_transactions_by_email_user_not_found():
    url = reverse("transactions-list") + "summary/?user_email=nonexistent@test.com"
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Not found."}
