import pytest
from unittest.mock import AsyncMock

from domain.entities import User
from domain.entities.enums import UserStatusEnum
from domain.dto.context import UserContextDTO
from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO, AdminDTO
from application.usecases.user import (
    DropUserUseCase,
    BanUserUseCase,
    ApproveUserUseCase,
    DisapproveUserUseCase,
    GetUserWithRoleUseCase,
    GetPendingUserUseCase
)
from application.external.notification import UserNotificationService
from application.dto.notification import (
    RegistrationApprovedNotificationDTO,
    RegistrationDisapprovedNotificationDTO,
    UserDroppedNotificationDTO,
    UserBannedNotificationDTO,
    AdminContactNotificationDTO
)
from application.services.user import (
    AdminUserManagementServiceImpl,
    AdminUserApprovalServiceImpl,
    AdminUserQueryServiceImpl,
    AdminUserNotificationServiceImpl
)
from tests.factories import UserFactory, ContracteeFactory, ContractorFactory, AdminFactory, ModelBaseFactory

# Настройка моков для AdminUserManagementServiceImpl
def setup_management_mocks(
    service: AdminUserManagementServiceImpl,
    user=None
):
    service.drop_user_use_case.drop_user.return_value = user
    service.ban_user_use_case.ban_user.return_value = user
    return service

# Настройка моков для AdminUserApprovalServiceImpl
def setup_approval_mocks(
    service: AdminUserApprovalServiceImpl,
    user=None
):
    service.approve_user_use_case.approve_user.return_value = user
    service.disapprove_user_use_case.disapprove_user.return_value = user
    return service

# Настройка моков для AdminUserQueryServiceImpl
def setup_query_mocks(
    service: AdminUserQueryServiceImpl,
    user=None
):
    service.get_user_use_case.get_user_with_role.return_value = user
    service.get_pending_user_use_case.get_pending_user.return_value = user
    return service

# Настройка моков для AdminUserNotificationServiceImpl
def setup_notification_mocks(
    service: AdminUserNotificationServiceImpl
):
    return service

@pytest.fixture
def drop_user_use_case():
    return AsyncMock(spec=DropUserUseCase)

@pytest.fixture
def ban_user_use_case():
    return AsyncMock(spec=BanUserUseCase)

@pytest.fixture
def approve_user_use_case():
    return AsyncMock(spec=ApproveUserUseCase)

@pytest.fixture
def disapprove_user_use_case():
    return AsyncMock(spec=DisapproveUserUseCase)

@pytest.fixture
def get_user_with_role_use_case():
    return AsyncMock(spec=GetUserWithRoleUseCase)

@pytest.fixture
def get_pending_user_use_case():
    return AsyncMock(spec=GetPendingUserUseCase)

@pytest.fixture
def notification_service():
    return AsyncMock(spec=UserNotificationService)

@pytest.fixture
def context():
    return UserContextDTO.model_validate(AdminFactory.get_random_data())

def generate_user_test_case(factory: type[ModelBaseFactory], dto: type[UserDTO]) -> tuple[User, UserDTO]:
    model = factory.create_model()
    expected_dto = dto.from_model(model)
    return model, expected_dto

# Тестовые данные для методов с ролями
get_user_with_role_test_data = [
    generate_user_test_case(ContracteeFactory, ContracteeDTO),
    generate_user_test_case(ContractorFactory, ContractorDTO),
    generate_user_test_case(AdminFactory, AdminDTO),
]

get_pending_user_test_data = [
    generate_user_test_case(ContracteeFactory, ContracteeDTO),
    generate_user_test_case(ContractorFactory, ContractorDTO),
]

class TestAdminUserManagementServiceImpl:
    @pytest.fixture
    def service(self, drop_user_use_case, ban_user_use_case, notification_service):
        return AdminUserManagementServiceImpl(
            drop_user_use_case=drop_user_use_case,
            ban_user_use_case=ban_user_use_case,
            notification_service=notification_service
        )

    @pytest.mark.asyncio
    async def test_drop_user_success(
        self,
        service: AdminUserManagementServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_management_mocks(service, user=expected)

        result = await service.drop_user(user.user_id, context)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_ban_user_success(
        self,
        service: AdminUserManagementServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_management_mocks(service, user=expected)

        result = await service.ban_user(user.user_id, context)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_drop_user_calls(
        self,
        service: AdminUserManagementServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_management_mocks(service, user=expected)

        await service.drop_user(user.user_id, context)

        service.drop_user_use_case.drop_user.assert_awaited_once_with(user.user_id)
        service.notification_service.send_user_dropped_notification.assert_awaited_once_with(
            UserDroppedNotificationDTO(receiver_id=user.user_id, executor_id=context.user_id)
        )

    @pytest.mark.asyncio
    async def test_ban_user_calls(
        self,
        service: AdminUserManagementServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_management_mocks(service, user=expected)

        await service.ban_user(user.user_id, context)

        service.ban_user_use_case.ban_user.assert_awaited_once_with(user.user_id)
        service.notification_service.send_user_banned_notification.assert_awaited_once_with(
            UserBannedNotificationDTO(receiver_id=user.user_id, executor_id=context.user_id)
        )

class TestAdminUserApprovalServiceImpl:
    @pytest.fixture
    def service(self, approve_user_use_case, disapprove_user_use_case, notification_service):
        return AdminUserApprovalServiceImpl(
            approve_user_use_case=approve_user_use_case,
            disapprove_user_use_case=disapprove_user_use_case,
            notification_service=notification_service
        )

    @pytest.mark.asyncio
    async def test_approve_registration_success(
        self,
        service: AdminUserApprovalServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_approval_mocks(service, user=expected)

        result = await service.approve_registration(user.user_id, context)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_disapprove_registration_success(
        self,
        service: AdminUserApprovalServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_approval_mocks(service, user=expected)

        result = await service.disapprove_registration(user.user_id, context)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_approve_registration_notification_is_called(
        self,
        service: AdminUserApprovalServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_approval_mocks(service, user=expected)

        await service.approve_registration(user.user_id, context)

        service.approve_user_use_case.approve_user.assert_awaited_once_with(user.user_id)
        service.notification_service.send_registration_approved_notification.assert_awaited_once_with(
            RegistrationApprovedNotificationDTO(receiver_id=user.user_id, executor_id=context.user_id)
        )

    @pytest.mark.asyncio
    async def test_disapprove_registration_notification_is_called(
        self,
        service: AdminUserApprovalServiceImpl,
        context: UserContextDTO
    ):
        user, _ = generate_user_test_case(UserFactory, UserDTO)
        setup_approval_mocks(service, user=user)

        await service.disapprove_registration(user.user_id, context)

        service.disapprove_user_use_case.disapprove_user.assert_awaited_once_with(user.user_id)
        service.notification_service.send_registration_disapproved_notification.assert_awaited_once_with(
            RegistrationDisapprovedNotificationDTO(receiver_id=user.user_id, executor_id=context.user_id)
        )


class TestAdminUserQueryServiceImpl:
    @pytest.fixture
    def service(self, get_user_with_role_use_case, get_pending_user_use_case):
        return AdminUserQueryServiceImpl(
            get_user_use_case=get_user_with_role_use_case,
            get_pending_user_use_case=get_pending_user_use_case
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user, expected", get_user_with_role_test_data)
    async def test_get_user_success(
        self,
        service: AdminUserQueryServiceImpl,
        user,
        expected
    ):
        setup_query_mocks(service, user=expected)

        result = await service.get_user(user.user_id)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_user_not_found(
        self,
        service: AdminUserQueryServiceImpl
    ):
        setup_query_mocks(service, user=None)

        result = await service.get_user(999)

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user, expected", get_pending_user_test_data)
    async def test_get_pending_user_success(
        self,
        service: AdminUserQueryServiceImpl,
        user,
        expected
    ):
        user.status = UserStatusEnum.pending
        expected.status = UserStatusEnum.pending
        setup_query_mocks(service, user=expected)

        result = await service.get_pending_user()

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_pending_user_not_found(
        self,
        service: AdminUserQueryServiceImpl
    ):
        setup_query_mocks(service, user=None)

        result = await service.get_pending_user()

        assert result is None

    @pytest.mark.asyncio
    async def test_get_user_calls(
        self,
        service: AdminUserQueryServiceImpl
    ):
        setup_query_mocks(service)
        await service.get_user(1)

        service.get_user_use_case.get_user_with_role.assert_awaited_once_with(1)

    @pytest.mark.asyncio
    async def test_get_pending_user_use_case_is_called(
        self,
        service: AdminUserQueryServiceImpl
    ):
        setup_query_mocks(service)
        await service.get_pending_user()

        service.get_pending_user_use_case.get_pending_user.assert_awaited_once()

class TestAdminUserNotificationServiceImpl:
    @pytest.fixture
    def service(self, notification_service):
        return AdminUserNotificationServiceImpl(notification_service=notification_service)

    @pytest.mark.asyncio
    async def test_notify_user_success(
        self,
        service: AdminUserNotificationServiceImpl,
        context: UserContextDTO
    ):
        user_id = 1
        setup_notification_mocks(service)
        result = await service.notify_user(user_id, context)

        # Здесь нет возвращаемого значения для проверки
        assert result is None

    @pytest.mark.asyncio
    async def test_notify_user_is_called(
        self,
        service: AdminUserNotificationServiceImpl,
        context: UserContextDTO
    ):
        user_id = 1
        setup_notification_mocks(service)
        await service.notify_user(user_id, context)

        service.notification_service.send_admin_contact_notification.assert_awaited_once_with(
            AdminContactNotificationDTO(receiver_id=user_id, executor_id=context.user_id)
        )