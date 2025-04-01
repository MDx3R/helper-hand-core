import pytest
from unittest.mock import AsyncMock

from application.usecases.user import (
    ApproveUserUseCase, 
    DisapproveUserUseCase, 
    DropUserUseCase, 
    BanUserUseCase,
    ChangeUserStatusUseCaseFacade
)

from domain.repositories import UserRepository
from domain.dto.common import UserDTO
from domain.entities import User
from domain.entities.enums import UserStatusEnum, RoleEnum
from domain.exceptions.service import NotFoundException, UserStatusChangeNotAllowedException

from tests.factories import UserFactory

from ..conftest import set_transactional

def create_user(user_id=1, status=UserStatusEnum.registered, role=RoleEnum.contractee):
    return UserFactory.create_model(user_id=user_id, status=status, role=role)

def setup_repository(repository: AsyncMock, user: User):
    async def change_user_status(
        user_id: int, status: UserStatusEnum
    ) -> User:
        return User.model_copy(user, update={"status": status})
    
    repository.get_user.return_value = user
    repository.change_user_status.side_effect = change_user_status
    return repository


def setup_repository_no_user(repository: AsyncMock):
    repository.get_user.return_value = None
    return repository


@pytest.fixture
def user_repository():
    return AsyncMock()


@pytest.fixture
def use_case(user_repository):
    return ChangeUserStatusUseCaseFacade(user_repository)

@pytest.fixture
def approve_use_case(use_case):
    return use_case


@pytest.fixture
def disapprove_use_case(use_case):
    return use_case


@pytest.fixture
def drop_use_case(use_case):
    return use_case


@pytest.fixture
def ban_use_case(use_case):
    return use_case


class TestApproveUserUseCase:
    @pytest.mark.asyncio
    async def test_approve_user(
        self,
        approve_use_case: ApproveUserUseCase, 
        user_repository: UserRepository
    ):
        user = create_user(status=UserStatusEnum.pending)
        setup_repository(user_repository, user)

        result = await approve_use_case.approve_user(user.user_id)

        assert result.status == UserStatusEnum.registered

    @pytest.mark.asyncio
    async def test_user_not_found(
        self,
        approve_use_case: ApproveUserUseCase, 
        user_repository: UserRepository
    ):
        setup_repository_no_user(user_repository)

        with pytest.raises(NotFoundException):
            await approve_use_case.approve_user(999)

        user_repository.change_user_status.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status", 
        [
            UserStatusEnum.created, 
            UserStatusEnum.dropped, 
            UserStatusEnum.banned, 
            UserStatusEnum.disapproved, 
            UserStatusEnum.registered
        ]
    )
    async def test_user_can_not_be_approved(
        self,
        approve_use_case: ApproveUserUseCase, 
        user_repository: UserRepository,
        status: UserStatusEnum
    ):
        user = create_user(status=status)
        setup_repository(user_repository, user)

        with pytest.raises(UserStatusChangeNotAllowedException):
            await approve_use_case.approve_user(user.user_id)

        user_repository.change_user_status.assert_not_awaited()

        
class TestDisapproveUserUseCase:
    @pytest.mark.asyncio
    async def test_disapprove_user(
        self, 
        disapprove_use_case: DisapproveUserUseCase, 
        user_repository: UserRepository
    ):
        user = create_user(status=UserStatusEnum.pending)
        setup_repository(user_repository, user)

        result = await disapprove_use_case.disapprove_user(user.user_id)

        assert result.status == UserStatusEnum.disapproved

    @pytest.mark.asyncio
    async def test_user_not_found(
        self,
        disapprove_use_case: DisapproveUserUseCase, 
        user_repository: UserRepository
    ):
        setup_repository_no_user(user_repository)

        with pytest.raises(NotFoundException):
            await disapprove_use_case.disapprove_user(999)

        user_repository.change_user_status.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status", 
        [
            UserStatusEnum.created, 
            UserStatusEnum.dropped, 
            UserStatusEnum.banned, 
            UserStatusEnum.disapproved, 
            UserStatusEnum.registered
        ]
    )
    async def test_user_can_not_be_disapproved(
        self,
        disapprove_use_case: DisapproveUserUseCase, 
        user_repository: UserRepository,
        status: UserStatusEnum
    ):
        user = create_user(status=status)
        setup_repository(user_repository, user)

        with pytest.raises(UserStatusChangeNotAllowedException):
            await disapprove_use_case.disapprove_user(user.user_id)

        user_repository.change_user_status.assert_not_awaited()


class TestDropUserUseCase:
    @pytest.mark.asyncio
    async def test_drop_user(
        self, 
        drop_use_case: DropUserUseCase, 
        user_repository: UserRepository
    ):
        user = create_user()
        setup_repository(user_repository, user)

        result = await drop_use_case.drop_user(user.user_id)

        assert result.status == UserStatusEnum.dropped

    @pytest.mark.asyncio
    async def test_user_not_found(
        self,
        drop_use_case: DropUserUseCase, 
        user_repository: UserRepository
    ):
        setup_repository_no_user(user_repository)

        with pytest.raises(NotFoundException):
            await drop_use_case.drop_user(999)

        user_repository.change_user_status.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_user_can_not_be_dropped(
        self,
        drop_use_case: DropUserUseCase, 
        user_repository: UserRepository,
    ):
        user = create_user(status=UserStatusEnum.dropped)
        setup_repository(user_repository, user)

        with pytest.raises(UserStatusChangeNotAllowedException):
            await drop_use_case.drop_user(user.user_id)

        user_repository.change_user_status.assert_not_awaited()


class TestBanUserUseCase:
    @pytest.mark.asyncio
    async def test_ban_user(
        self, 
        ban_use_case: BanUserUseCase, 
        user_repository: UserRepository
    ):
        user = create_user()
        setup_repository(user_repository, user)

        result = await ban_use_case.ban_user(user.user_id)

        assert result.status == UserStatusEnum.banned

    @pytest.mark.asyncio
    async def test_user_not_found(
        self,
        ban_use_case: BanUserUseCase, 
        user_repository: UserRepository
    ):
        setup_repository_no_user(user_repository)

        with pytest.raises(NotFoundException):
            await ban_use_case.ban_user(999)

        user_repository.change_user_status.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_user_can_not_be_banned(
        self,
        ban_use_case: BanUserUseCase, 
        user_repository: UserRepository,
    ):
        user = create_user(status=UserStatusEnum.banned)
        setup_repository(user_repository, user)

        with pytest.raises(UserStatusChangeNotAllowedException):
            await ban_use_case.ban_user(user.user_id)

        user_repository.change_user_status.assert_not_awaited()

class TestChangeAdminStatusUseCase:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status", 
        [
            UserStatusEnum.dropped, 
            UserStatusEnum.banned, 
            UserStatusEnum.disapproved, # admin не может быть pending 
            UserStatusEnum.registered # admin не может быть pending 
        ]
    )
    async def test_admin_status_cannot_be_changed(
        self,
        use_case: ChangeUserStatusUseCaseFacade,
        user_repository: UserRepository,
        status: UserStatusEnum
    ):
        user = create_user(role=RoleEnum.admin)
        setup_repository(user_repository, user)

        with pytest.raises(UserStatusChangeNotAllowedException):
            await use_case.change_user_status(user.user_id, status)

        user_repository.change_user_status.assert_not_awaited()

class TestChangeUserStatusUseCaseCalls:
    @pytest.mark.asyncio
    async def test_repository_calls(
        self, 
        use_case: ChangeUserStatusUseCaseFacade, 
        user_repository: UserRepository,
    ):
        user = create_user()
        setup_repository(user_repository, user)

        await use_case.change_user_status(user.user_id, UserStatusEnum.dropped)

        user_repository.get_user.assert_awaited_once_with(user.user_id)
        user_repository.change_user_status.assert_awaited_once()
