from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category, Customer, Transaction


def get_user_id(email):
    user, _ = Customer.objects.get_or_create(**email)
    return user.id


def get_category_id(name):
    category, _ = Category.objects.get_or_create(**name)
    return category.id


class TransactionSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    user_email = serializers.CharField(source="user.email", required=True)
    type = serializers.CharField(source="kind")
    reference = serializers.CharField(
        max_length=50, validators=[UniqueValidator(queryset=Transaction.objects.all())]
    )

    def validate_user_email(self, value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid e-mail format")
        else:
            return value

    def save(self):
        validated_data = self.validated_data

        user_email = validated_data.pop("user")
        user_id = get_user_id(user_email)

        category_name = validated_data.pop("category")
        category_id = get_category_id(category_name)

        validated_data |= {"user_id": user_id, "category_id": category_id}

        return super().save()

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
