from concurrent.futures import ThreadPoolExecutor

from src.models import Transaction
from tests.factories import CategoryFactory, CustomerFactory

customer = CustomerFactory.create(email="dev@test.com")

category_a = CategoryFactory.create(name="category-A")
category_b = CategoryFactory.create(name="category-B")


def create_inflow_category_a():
    instances = []
    for item in range(0, 800000):
        instances.append(
            Transaction(
                reference=str(item),
                date="2022-10-10",
                amount="100.00",
                type="inflow",
                category=category_a,
                user=customer,
            )
        )
        if item % 500 == 0:
            Transaction.objects.bulk_create(instances)
            instances = []


def create_outflow_category_a():
    instances = []
    for item in range(800000, 1600000):
        instances.append(
            Transaction(
                reference=str(item),
                date="2022-10-10",
                amount="-100.00",
                type="outflow",
                category=category_a,
                user=customer,
            )
        )
        if item % 500 == 0:
            Transaction.objects.bulk_create(instances)
            instances = []


def create_inflow_category_b():
    instances = []
    for item in range(1600000, 2400000):
        instances.append(
            Transaction(
                reference=str(item),
                date="2022-10-10",
                amount="1000.00",
                type="inflow",
                category=category_b,
                user=customer,
            )
        )
        if item % 500 == 0:
            Transaction.objects.bulk_create(instances)
            instances = []


def create_outflow_category_b():
    instances = []
    for item in range(2400000, 3200000):
        instances.append(
            Transaction(
                reference=str(item),
                date="2022-10-10",
                amount="-1000.00",
                type="outflow",
                category=category_b,
                user=customer,
            )
        )
        if item % 500 == 0:
            Transaction.objects.bulk_create(instances)
            instances = []


with ThreadPoolExecutor(max_workers=4) as executor:
    executor.submit(create_inflow_category_a)
    executor.submit(create_outflow_category_a)
    executor.submit(create_inflow_category_b)
    executor.submit(create_outflow_category_b)
