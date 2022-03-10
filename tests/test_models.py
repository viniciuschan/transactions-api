from .factories import CategoryFactory, CustomerFactory
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
