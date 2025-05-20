from unittest.mock import AsyncMock

import pytest

from infrastructure.repositories.base import QueryExecutor


@pytest.fixture
def query_executor():
    return AsyncMock(QueryExecutor)
