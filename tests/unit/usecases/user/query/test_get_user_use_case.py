import pytest

from domain.repositories import UserRepository
from domain.dto.internal import GetUserDTO

from application.usecases.user import (
    UserQueryUseCaseFacade
)
from .conftest import (
    UserFactory,
    UserDTO,
    setup_repository,
    generate_user_test_case
)

class TestGetUserUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    async def test_get_user_success(
        self, 
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository,
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_repository(user_repository, user)

        result = await use_case.get_user(
            GetUserDTO(user_id=user.user_id)
        )

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_user_not_found(
        self, 
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_user(
            GetUserDTO(user_id=999)
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_get_user_is_called(
        self, 
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository
    ):
        await use_case.get_user(GetUserDTO(user_id=1))

        user_repository.get_user.assert_awaited_once_with(1)