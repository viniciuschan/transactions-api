import factory
from factory.django import DjangoModelFactory

from src.models import Category, Customer, Transaction


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = "Belvo"


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    email = "dev@test.com"
    salary = "5000.00"


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    class Params:
        profile = factory.SubFactory(CustomerFactory)
        categ = factory.SubFactory(CategoryFactory)

    reference = ("000001",)
    date = "2022-03-08"
    amount = "500.00"
    kind = ("IN",)
    category = factory.SelfAttribute("categ")
    user = factory.SelfAttribute("profile")
