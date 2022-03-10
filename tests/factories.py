import factory
from factory.django import DjangoModelFactory
from faker import Faker

from src.models import Category, Customer, Transaction

fake = Faker()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = fake.slug()


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer
        django_get_or_create = ("email",)

    email = fake.email()


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = Transaction

    class Params:
        profile = factory.SubFactory(CustomerFactory)
        categ = factory.SubFactory(CategoryFactory)

    reference = fake.numerify()
    date = "2022-03-08"
    amount = "500.00"
    kind = Transaction.Type.INFLOW
    category = factory.SelfAttribute("categ")
    user = factory.SelfAttribute("profile")
