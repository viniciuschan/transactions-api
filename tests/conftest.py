import pytest

from src.models import Transaction


@pytest.fixture
def transaction_payload():
    return {
        "reference": "123456098765",
        "date": "2020-01-03",
        "amount": "500.00",
        "type": Transaction.Type.INFLOW,
        "category": "any_category",
        "user_email": "fixture@test.com",
    }
