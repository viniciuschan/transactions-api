from django.conf import settings
from rest_framework import serializers

from . import logger
from .models import Category, Customer, Transaction


def get_user_id(email):
    user, _ = Customer.objects.get_or_create(**email)
    return user.id


def get_category_id(name):
    category, _ = Category.objects.get_or_create(**name)
    return category.id


class CustomTransactionSerializer(serializers.ModelSerializer):
    type = serializers.CharField(max_length=7, required=True)
    category = serializers.CharField(source="category.name", max_length=30, required=True)
    user_email = serializers.EmailField(source="user.email", max_length=30, required=True)
    reference = serializers.CharField(max_length=20, required=True)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateField()

    def validate_type(self, value):
        if value not in Transaction.Types:
            raise serializers.ValidationError("Invalid transaction type.")
        return value

    def _validate_transaction(self, transaction_type, amount, reference):
        match transaction_type:
            case Transaction.INFLOW:
                if amount < 0:
                    logger.warning(f"The transaction amount from reference={reference} must be positive.")
                    raise serializers.ValidationError("Inflow transactions must have postive amount.")
            case Transaction.OUTFLOW:
                if amount > 0:
                    logger.warning(f"The transaction amount from reference={reference} must be negative.")
                    raise serializers.ValidationError("Outflow transactions must have negative amount.")

    def validate(self, data):
        transaction_type, amount, reference = data["type"], data["amount"], data["reference"]
        self._validate_transaction(transaction_type, amount, reference)
        return super().validate(data)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "reference",
            "date",
            "amount",
            "type",
            "category",
            "user_email",
        )


class TransactionSerializer(CustomTransactionSerializer):
    def validate_reference(self, value):
        if Transaction.objects.filter(reference=value).exists():
            logger.warning(f"Reference={value} already exists.")
            raise serializers.ValidationError("Reference={value} already exists.")
        return value

    def save(self, **kwargs):
        validated_data = self.validated_data

        user_email = validated_data.pop("user")
        user_id = get_user_id(user_email)

        category = validated_data.pop("category")
        category_id = get_category_id(category)

        validated_data |= {"user_id": user_id, "category_id": category_id}

        return super().save()


class TransactionBulkCreateSerializer(serializers.Serializer):
    payload = CustomTransactionSerializer(many=True)

    def create(self, validated_data):
        data = validated_data["payload"]

        instances = []
        for item in data:
            category_id = get_category_id(item["category"])
            user_id = get_user_id(item["user"])

            instance = Transaction(
                reference=item["reference"],
                date=item["date"],
                amount=item["amount"],
                type=item["type"],
                category_id=category_id,
                user_id=user_id,
            )
            instances.append(instance)

        return Transaction.objects.bulk_create(
            instances,
            batch_size=settings.BULK_CREATE_BATCH_SIZE,
            ignore_conflicts=True,
        )
