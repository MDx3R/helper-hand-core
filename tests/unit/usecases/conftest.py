import pytest
from unittest.mock import AsyncMock

from application.transactions import TransactionManager
from application.transactions.configuration import set_transaction_manager

@pytest.fixture(scope="session")
def transaction_manager():
    mock = AsyncMock()

    mock.__aenter__ = AsyncMock(return_value=None)
    mock.__aexit__ = AsyncMock(return_value=None)
    return mock

@pytest.fixture(scope="session", autouse=True)
def set_transactional(transaction_manager: TransactionManager):
    set_transaction_manager(transaction_manager)