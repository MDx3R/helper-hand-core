import pytest

from application.usecases.user import UserQueryUseCaseFacade
from application.usecases.user.user_query_use_case import GetUserUseCase
from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_query_dto import GetUserDTO
from domain.dto.user.response.user_output_dto import UserOutputDTO
from domain.entities.user.user import User
from domain.repositories.user.user_query_repository import UserQueryRepository
from tests.data_generators import UserDataGenerator
from tests.factories import UserFactory, UserOutputDTOFactory
from .conftest import setup_repository

gen = UserDataGenerator()


class TestGetUserUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    async def test_get_user_success(
        self,
        use_case: GetUserUseCase,
        user_repository: UserQueryRepository,
    ):
        # Arrange
        user = UserFactory(gen).create_default()
        expected = UserOutputDTOFactory(gen).create()

        setup_repository(user_repository, user)

        # Act
        result = await use_case.execute(GetUserDTO(user_id=user.user_id))

        # Assert
        assert isinstance(result, UserOutputDTO)
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_user_not_found(
        self,
        use_case: GetUserUseCase,
        user_repository: UserQueryRepository,
    ):
        user_id = 999

        setup_repository(user_repository, None)

        result = await use_case.execute(GetUserDTO(user_id=user_id))

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user", [None, UserFactory(gen).create_default()])
    async def test_get_user_is_called_properly(
        self,
        use_case: GetUserUseCase,
        user_repository: UserQueryRepository,
        user: User,
    ):
        user_id = 999 if not user else user.user_id

        setup_repository(user_repository, user)

        await use_case.execute(GetUserDTO(user_id=user_id))

        user_repository.get_user.assert_awaited_once_with(
            UserIdDTO(user_id=user.user_id)
        )
