import pytest

from domain.repositories import UserRepository
from domain.entities.enums import UserStatusEnum

from application.usecases.user import (
    UserQueryUseCaseFacade
)
from .conftest import (
    setup_repository,
    get_pending_user_test_data
)

class TestGetPendingUserUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user, expected", get_pending_user_test_data)
    async def test_get_pending_user_success(
        self, 
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository,
        user, 
        expected
    ):
        user.status = UserStatusEnum.pending
        expected.status = UserStatusEnum.pending
        setup_repository(user_repository, user)

        result = await use_case.get_pending_user()

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_pending_user_not_found(
        self, 
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_pending_user()

        assert result is None

    @pytest.mark.asyncio
    async def test_get_pending_user_is_called(
        self, 
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository
    ):
        await use_case.get_pending_user()

        user_repository.get_first_pending_user_with_role.assert_awaited_once()