import pytest
from unittest.mock import AsyncMock

from domain.dto.user.internal.user_filter_dto import UserFilterDTO
from domain.entities.user.user import User
from infrastructure.database.models import UserBase
from infrastructure.repositories.user.user_query_repository import (
    UserQueryRepositoryImpl,
)
from infrastructure.repositories.base import QueryExecutor
from tests.data_generators import UserDataGenerator
from tests.factories import UserFactory


class TestUserQueryRepositoryImpl:
    """Тестовый набор для класса UserQueryRepositoryImpl."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Настроить тестовую среду с поддельными зависимостями."""
        self.mock_executor = AsyncMock(QueryExecutor)
        self.repository = UserQueryRepositoryImpl(self.mock_executor)

    def _get_base(self) -> UserBase:
        return UserBase.base_validate(self._get_user().model_dump())

    def _get_user(self) -> User:
        gen = UserDataGenerator()
        factory = UserFactory(gen)
        return factory.create_default()

    # Вспомогательные методы для настройки моков
    def _setup_executor_scalar_one(self, return_value):
        """Настроить возвращаемое значение для execute_scalar_one."""
        self.mock_executor.execute_scalar_one.return_value = return_value

    def _setup_executor_scalar_many(self, return_value):
        """Настроить возвращаемое значение для execute_scalar_many."""
        self.mock_executor.execute_scalar_many.return_value = return_value

    @pytest.mark.asyncio
    async def test_get_user_returns_user_when_exists(self):
        """Проверить, что get_user возвращает User, если пользователь существует."""
        user_base = self._get_base()
        user_id = user_base.user_id
        self._setup_executor_scalar_one(user_base)

        result = await self.repository.get_user(user_id)

        self.mock_executor.execute_scalar_one.assert_awaited_once()
        assert isinstance(result, User)
        assert result.user_id == user_id
        assert result.name == user_base.name

    @pytest.mark.asyncio
    async def test_get_user_returns_none_when_user_does_not_exist(self):
        """Проверить, что get_user возвращает None, если пользователь не найден."""
        user_id = 1
        self._setup_executor_scalar_one(None)

        result = await self.repository.get_user(user_id)

        self.mock_executor.execute_scalar_one.assert_awaited_once()
        assert result is None

    @pytest.mark.asyncio
    async def test_filter_users_returns_list_of_users(self):
        """Проверить, что filter_users возвращает список пользователей, если найдены совпадения."""
        query = UserFilterDTO(name="Test")
        user_bases = [self._get_base() for _ in range(3)]
        self._setup_executor_scalar_many(user_bases)

        result = await self.repository.filter_users(query)

        self.mock_executor.execute_scalar_many.assert_awaited_once()
        assert len(result) == 3
        assert all(isinstance(user, User) for user in result)
        assert [user.user_id for user in result] == [
            user.user_id for user in user_bases
        ]
        assert [user.name for user in result] == [
            user.name for user in user_bases
        ]

    @pytest.mark.asyncio
    async def test_filter_users_returns_empty_list_when_no_matches(self):
        """Проверить, что filter_users возвращает пустой список, если нет совпадений."""
        query = UserFilterDTO(name="Nonexistent")
        self._setup_executor_scalar_many([])

        result = await self.repository.filter_users(query)

        self.mock_executor.execute_scalar_many.assert_awaited_once()
        assert result == []

    @pytest.mark.asyncio
    async def test_exists_by_query_returns_true_when_user_exists(self):
        """Проверить, что exists_by_query возвращает True, если пользователь найден по запросу."""
        query = UserFilterDTO(name="Test")
        user_base = self._get_base()
        self._setup_executor_scalar_one(user_base)

        result = await self.repository.exists_by_query(query)

        self.mock_executor.execute_scalar_one.assert_awaited_once()
        assert result is True

    @pytest.mark.asyncio
    async def test_exists_by_query_returns_false_when_no_user_exists(self):
        """Проверить, что exists_by_query возвращает False, если пользователь не найден по запросу."""
        query = UserFilterDTO(name="Nonexistent")
        self._setup_executor_scalar_one(None)

        result = await self.repository.exists_by_query(query)

        self.mock_executor.execute_scalar_one.assert_awaited_once()
        assert result is False
