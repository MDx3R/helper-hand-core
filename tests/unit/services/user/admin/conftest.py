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