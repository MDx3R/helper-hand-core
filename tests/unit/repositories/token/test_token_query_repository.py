import pytest

from domain.dto.token import TokenFilter, TokenSignature
from domain.entities.token.token import Token
from infrastructure.repositories.token.token_query_repository import (
    TokenQueryRepositoryImpl,
)

from .conftest import get_token, get_base


class TestTokenQueryRepositoryImpl:
    """Тестовый набор для класса TokenQueryRepositoryImpl."""

    @pytest.fixture(autouse=True)
    def setup(self, query_executor):
        """Настроить тестовую среду с поддельными зависимостями."""
        self.mock_executor = query_executor
        self.repository = TokenQueryRepositoryImpl(self.mock_executor)

    def _setup_executor_scalar_one(self, return_value):
        """Настроить возвращаемое значение для execute_scalar_one."""
        self.mock_executor.execute_scalar_one.return_value = return_value

    def _setup_executor_scalar_many(self, return_value):
        """Настроить возвращаемое значение для execute_scalar_many."""
        self.mock_executor.execute_scalar_many.return_value = return_value

    @pytest.mark.asyncio
    async def test_get_token_returns_token_when_exists(self):
        """Проверить, что get_token возвращает Token, если токен существует."""
        token_base = get_base()
        signature = TokenSignature(token=token_base.token)
        self._setup_executor_scalar_one(token_base)

        result = await self.repository.get_token(signature)

        self.mock_executor.execute_scalar_one.assert_awaited_once()
        assert isinstance(result, Token)
        assert result.token == token_base.token
        assert result.user_id == token_base.user_id

    @pytest.mark.asyncio
    async def test_get_token_returns_none_when_token_does_not_exist(self):
        """Проверить, что get_token возвращает None, если токен не найден."""
        signature = TokenSignature(token="notfound")
        self._setup_executor_scalar_one(None)

        result = await self.repository.get_token(signature)

        self.mock_executor.execute_scalar_one.assert_awaited_once()
        assert result is None

    @pytest.mark.asyncio
    async def test_filter_tokens_returns_list_of_tokens(self):
        """Проверить, что filter_tokens возвращает список токенов, если найдены совпадения."""
        query = TokenFilter(user_id=1)
        token_bases = [get_base() for _ in range(2)]
        self._setup_executor_scalar_many(token_bases)

        result = await self.repository.get_tokens(query)

        self.mock_executor.execute_scalar_many.assert_awaited_once()
        assert len(result) == 2
        assert all(isinstance(token, Token) for token in result)
        assert [token.token for token in result] == [
            b.token for b in token_bases
        ]
        assert [token.user_id for token in result] == [
            b.user_id for b in token_bases
        ]

    @pytest.mark.asyncio
    async def test_filter_tokens_returns_empty_list_when_no_matches(self):
        """Проверить, что filter_tokens возвращает пустой список, если нет совпадений."""
        query = TokenFilter(user_id=999)
        self._setup_executor_scalar_many([])

        result = await self.repository.get_tokens(query)

        self.mock_executor.execute_scalar_many.assert_awaited_once()
        assert result == []
