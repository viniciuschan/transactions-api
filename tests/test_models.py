import pytest

from .factories import CategoryFactory, CustomerFactory, TransactionFactory
from src.models import Category, Customer, Transaction


def test_create_transaction():
    category = CategoryFactory.create()
    customer = CustomerFactory.create()

    transaction = Transaction.objects.create(
        reference="000001",
        date="2022-03-08",
        amount="500.00",
        kind=Transaction.Type.INFLOW,
        user=customer,
        category=category,
    )
    assert isinstance(transaction, Transaction)
    assert str(transaction) == f"Transaction({transaction.reference})"


def test_create_category():
    category = Category.objects.create(
        name="groceries",
    )
    assert isinstance(category, Category)
    assert str(category) == f"Category({category.name})"


def test_create_customer():
    customer = Customer.objects.create(
        email="dev@test.com",
    )
    assert isinstance(customer, Customer)
    assert str(customer) == f"Customer({customer.email})"


def test_soft_delete_transaction_instance():
    transaction = TransactionFactory.create()
    transaction.delete()

    with pytest.raises(Transaction.DoesNotExist):
        Transaction.objects.get(id=transaction.id)

    deleted = Transaction.objects.deleteds().get(id=transaction.id)
    assert deleted.deleted_at is not None


def test_undelete_transaction_instance():
    transaction = TransactionFactory.create(deleted_at="2022-03-10T21:33:45.116852Z")
    assert Transaction.objects.exists() is False

    transaction.undelete()
    transaction.refresh_from_db()
    assert transaction.deleted_at is None
    assert Transaction.objects.exists() is True


def test_ultra_hard_delete_transaction_instance():
    transaction = TransactionFactory.create()

    transaction.ultra_hard_delete()
    assert Transaction.objects.exists() is False
    assert Transaction.objects.deleteds().exists() is False


def test_soft_delete_transaction_queryset():
    TransactionFactory.create()

    qs = Transaction.objects.all()
    qs.delete()

    Transaction.objects.exists() is False
    Transaction.objects.deleteds().exists() is True


def test_undelete_transaction_queryset():
    transaction = TransactionFactory.create(deleted_at="2022-03-10T21:33:45.116852Z")
    assert Transaction.objects.exists() is False

    transaction.undelete()
    assert Transaction.objects.exists() is True
    assert Transaction.objects.deleteds().exists() is False


def test_ultra_hard_delete_transaction_queryset():
    TransactionFactory.create()

    qs = Transaction.objects.all()
    qs.ultra_hard_delete()

    assert Transaction.objects.exists() is False
    assert Transaction.objects.deleteds().exists() is False
