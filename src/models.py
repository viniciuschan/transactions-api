import uuid
from decimal import Decimal

from django.db import models
from model_utils import Choices

from .mixins import SoftDeleteModelMixin


class Transaction(SoftDeleteModelMixin):
    INFLOW = "inflow"
    OUTFLOW = "outflow"

    Types = Choices(
        (INFLOW, "Inflow"),
        (OUTFLOW, "Outflow"),
    )

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    reference = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal())
    type = models.CharField(max_length=7, choices=Types)
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    user = models.ForeignKey("Customer", on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{type(self).__name__}({self.reference})"


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{type(self).__name__}({self.name})"


class Customer(models.Model):
    email = models.EmailField(max_length=30, unique=True)

    def __str__(self):
        return f"{type(self).__name__}({self.email})"
