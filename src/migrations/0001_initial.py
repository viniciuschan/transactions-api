import uuid
from decimal import Decimal

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("email", models.EmailField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("deleted_at", models.DateTimeField(null=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("reference", models.CharField(max_length=20, unique=True)),
                ("date", models.DateField()),
                ("amount", models.DecimalField(decimal_places=2, default=Decimal("0"), max_digits=10)),
                (
                    "type",
                    models.CharField(choices=[("inflow", "Inflow"), ("outflow", "Outflow")], max_length=7),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "category",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="src.category"),
                ),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="src.customer")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
