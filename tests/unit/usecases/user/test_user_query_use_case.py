import pytest
from unittest.mock import AsyncMock

from application.usecases.user import (
    GetUserUseCase,
    GetUserWithRoleUseCase,
    GetAdminUseCase,
    GetContracteeUseCase,
    GetContractorUseCase,
    GetPendingUserUseCase,
    UserQueryUseCaseFacade
)
from domain.repositories import UserRepository
from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO, AdminDTO
from domain.entities import User, Contractee, Contractor, Admin
from domain.entities.enums import UserStatusEnum
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

class TestGetUserUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    async def test_get_user_success(
        self, 
        use_case: GetUserUseCase, 
        user_repository: UserRepository,
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_repository(user_repository, user)

        result = await use_case.get_user(user.user_id)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_user_not_found(
        self, 
        use_case: GetUserUseCase, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_user(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_user_is_called(
        self, 
        use_case: GetUserUseCase, 
        user_repository: UserRepository
    ):
        await use_case.get_user(1)

        user_repository.get_user.assert_awaited_once_with(1)

class TestGetUserWithRoleUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user, expected", get_user_with_role_test_data)
    async def test_get_user_with_role_success(
        self, 
        use_case: GetUserWithRoleUseCase, 
        user_repository: UserRepository,
        user, 
        expected
    ):
        setup_repository(user_repository, user)

        result = await use_case.get_user_with_role(user.user_id)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_user_with_role_not_found(
        self, 
        use_case: GetUserWithRoleUseCase, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_user_with_role(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_user_with_role_is_called(
        self, 
        use_case: GetUserWithRoleUseCase, 
        user_repository: UserRepository
    ):
        await use_case.get_user_with_role(1)

        user_repository.get_user_with_role.assert_awaited_once_with(1)

class TestGetPendingUserUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user, expected", get_pending_user_test_data)
    async def test_get_pending_user_success(
        self, 
        use_case: GetPendingUserUseCase, 
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
        use_case: GetPendingUserUseCase, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_pending_user()

        assert result is None

    @pytest.mark.asyncio
    async def test_get_pending_user_is_called(
        self, 
        use_case: GetPendingUserUseCase, 
        user_repository: UserRepository
    ):
        await use_case.get_pending_user()

        user_repository.get_first_pending_user_with_role.assert_awaited_once()

class TestGetAdminUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    async def test_get_admin_success(
        self, 
        use_case: GetAdminUseCase, 
        user_repository: UserRepository,
    ):
        admin, expected = generate_user_test_case(AdminFactory, AdminDTO)
        setup_repository(user_repository, admin)

        result = await use_case.get_admin(admin.user_id)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_admin_not_found(
        self, 
        use_case: GetAdminUseCase, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_admin(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_admin_is_called(
        self, 
        use_case: GetAdminUseCase, 
        user_repository: UserRepository
    ):
        await use_case.get_admin(1)

        user_repository.get_admin.assert_awaited_once_with(1)

class TestGetContracteeUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    async def test_get_contractee_success(
        self, 
        use_case: GetContracteeUseCase, 
        user_repository: UserRepository,
    ):
        contractee, expected = generate_user_test_case(ContracteeFactory, ContracteeDTO)
        setup_repository(user_repository, contractee)

        result = await use_case.get_contractee(contractee.user_id)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_contractee_not_found(
        self, 
        use_case: GetContracteeUseCase, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_contractee(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_contractee_is_called(
        self, 
        use_case: GetContracteeUseCase, 
        user_repository: UserRepository
    ):
        await use_case.get_contractee(1)

        user_repository.get_contractee.assert_awaited_once_with(1)

class TestGetContractorUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    async def test_get_contractor_success(
        self, 
        use_case: GetContractorUseCase, 
        user_repository: UserRepository,
    ):
        contractor, expected = generate_user_test_case(ContractorFactory, ContractorDTO)
        setup_repository(user_repository, contractor)

        result = await use_case.get_contractor(contractor.user_id)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_contractor_not_found(
        self, 
        use_case: GetContractorUseCase, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_contractor(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_contractor_is_called(
        self, 
        use_case: GetContractorUseCase, 
        user_repository: UserRepository
    ):
        await use_case.get_contractor(1)

        user_repository.get_contractor.assert_awaited_once_with(1)