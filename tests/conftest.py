import logging

import pytest
from _pytest.logging import caplog as _caplog  # noqa
from loguru import logger


# simple handler to test logs from loguru using pytest caplog fixture
@pytest.fixture
def caplog(_caplog):  # noqa
    class PropagateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropagateHandler(), format="{message}")
    yield _caplog
    logger.remove(handler_id)


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
