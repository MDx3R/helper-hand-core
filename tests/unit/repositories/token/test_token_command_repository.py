import pytest
from uuid import uuid4

from domain.entities.token.token import Token
from infrastructure.repositories.token.token_command_repository import (
    TokenCommandRepositoryImpl,
)

from .conftest import get_token, get_base


class TestTokenCommandRepositoryImpl:
    """Тестовый набор для класса TokenCommandRepositoryImpl."""

    @pytest.fixture(autouse=True)
    def setup(self, query_executor):
        """Настроить тестовую среду с поддельными зависимостями."""
        self.mock_executor = query_executor
        self.repository = TokenCommandRepositoryImpl(self.mock_executor)

    @pytest.mark.asyncio
    async def test_create_token_returns_token(self):
        """Проверить, что create_token возвращает созданный токен."""
        token = get_token()

        result = await self.repository.create_token(token)

        self.mock_executor.add.assert_awaited_once()
        assert isinstance(result, Token)
        assert result.token == token.token
        assert result.user_id == token.user_id

    @pytest.mark.asyncio
    async def test_revoke_token_returns_token_when_exists(self):
        """Проверить, что revoke_token возвращает токен, если он существует."""
        token_base = get_base()
        self.mock_executor.execute_scalar_one.return_value = token_base

        result = await self.repository.revoke_token(token_base.token)

        self.mock_executor.execute_scalar_one.assert_awaited_once()
        assert isinstance(result, Token)
        assert result.token == token_base.token
        assert result.revoked is False or result.revoked is True

    @pytest.mark.asyncio
    async def test_revoke_token_raises_not_found_when_token_does_not_exist(
        self,
    ):
        """Проверить, что revoke_token вызывает NotFoundException, если токен не найден."""
        from domain.exceptions.service.common import NotFoundException

        self.mock_executor.execute_scalar_one.return_value = None

        with pytest.raises(NotFoundException):
            await self.repository.revoke_token("notfound")

        self.mock_executor.execute_scalar_one.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_revoke_tokens_by_session_returns_list_of_tokens(self):
        """Проверить, что revoke_tokens_by_session возвращает список отозванных токенов."""
        session = uuid4()
        token_bases = [get_base() for _ in range(2)]
        self.mock_executor.execute_scalar_many.return_value = token_bases

        result = await self.repository.revoke_tokens_by_session(session)

        self.mock_executor.execute_scalar_many.assert_awaited_once()
        assert len(result) == 2
        assert all(isinstance(token, Token) for token in result)
        assert [token.token for token in result] == [
            b.token for b in token_bases
        ]
