import pytest


@pytest.fixture
def transaction_payload():
    return {
        "reference": "123456098765",
        "date": "2020-01-03",
        "amount": "500.00",
        "type": "inflow",
        "category": "any_category",
        "user_email": "fixture@test.com",
    }
