import pytest
from unittest.mock import AsyncMock

from domain.entities import User
from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO, AdminDTO

from tests.factories import UserFactory, ContracteeFactory, ContractorFactory, AdminFactory, ModelBaseFactory

def setup_repository(repository: AsyncMock, user=None):
    repository.get_user.return_value = user
    repository.get_user_with_role.return_value = user
    repository.get_admin.return_value = user
    repository.get_contractee.return_value = user
    repository.get_contractor.return_value = user
    repository.get_first_pending_user_with_role.return_value = user
    return repository

@pytest.fixture
def user_repository():
    repository = AsyncMock()
    return setup_repository(repository, None)

def generate_user_test_case(factory: type[ModelBaseFactory], dto: type[UserDTO]) -> tuple[User, UserDTO]:
    model = factory.create_model()
    expected_dto = dto.from_model(model)
    return model, expected_dto

# Тестовые данные для GetUserUseCase
get_user_test_data = [
    generate_user_test_case(UserFactory, UserDTO),
]

# Тестовые данные для GetUserWithRoleUseCase
get_user_with_role_test_data = [
    generate_user_test_case(ContracteeFactory, ContracteeDTO),
    generate_user_test_case(ContractorFactory, ContractorDTO),
    generate_user_test_case(AdminFactory, AdminDTO),
]

# Тестовые данные для GetPendingUserUseCase
get_pending_user_test_data = [
    generate_user_test_case(ContracteeFactory, ContracteeDTO),
    generate_user_test_case(ContractorFactory, ContractorDTO),
]