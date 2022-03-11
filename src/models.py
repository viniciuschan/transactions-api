import uuid
from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import SoftDeleteModelMixin


class Transaction(SoftDeleteModelMixin):
    class Type(models.TextChoices):
        INFLOW = "IN", _("Inflow")
        OUTFLOW = "OU", _("Outflow")

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    reference = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal())
    kind = models.CharField(max_length=2, choices=Type.choices)
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    user = models.ForeignKey("Customer", on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{type(self).__name__}({self.reference})"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{type(self).__name__}({self.name})"


class Customer(models.Model):
    email = models.EmailField(max_length=30, unique=True)

    def __str__(self):
        return f"{type(self).__name__}({self.email})"
