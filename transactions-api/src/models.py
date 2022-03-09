import uuid

from django.db import models


class Transaction(models.Model):
    FLOW_CHOICES = [
        ("IN", "Inflow"),
        ("OU", "Outflow"),
    ]

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )
    reference = models.CharField(max_length=20, unique=True)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    kind = models.CharField(max_length=2, choices=FLOW_CHOICES)
    category = models.ForeignKey("Category", on_delete=models.PROTECT)
    user = models.ForeignKey("Customer", on_delete=models.PROTECT)

    def __str__(self):
        return f"{type(self).__name__}({self.reference})"


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{type(self).__name__}({self.name})"


class Customer(models.Model):
    email = models.EmailField(max_length=30, unique=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{type(self).__name__}({self.email})"
