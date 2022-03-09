from factory.django import DjangoModelFactory

from src.models import Category, Customer


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = "Belvo"


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    email = "dev@test.com"
    salary = "5000.00"
