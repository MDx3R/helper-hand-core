import pytest

from domain.repositories import UserRepository
from application.usecases.user import (
    UserQueryUseCaseFacade
)
from .conftest import (
    AdminFactory,
    AdminDTO,
    ContracteeFactory,
    ContracteeDTO,
    ContractorFactory,
    ContractorDTO,
    setup_repository,
    generate_user_test_case,
    get_user_with_role_test_data
)

class TestGetUserWithRoleUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user, expected", get_user_with_role_test_data)
    async def test_get_user_with_role_success(
        self, 
        use_case: UserQueryUseCaseFacade, 
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
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_user_with_role(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_user_with_role_is_called(
        self, 
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository
    ):
        await use_case.get_user_with_role(1)

        user_repository.get_user_with_role.assert_awaited_once_with(1)

class TestGetAdminUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    async def test_get_admin_success(
        self, 
        use_case: UserQueryUseCaseFacade, 
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
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_admin(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_admin_is_called(
        self, 
        use_case: UserQueryUseCaseFacade, 
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
        use_case: UserQueryUseCaseFacade, 
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
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_contractee(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_contractee_is_called(
        self, 
        use_case: UserQueryUseCaseFacade, 
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
        use_case: UserQueryUseCaseFacade, 
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
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository
    ):
        setup_repository(user_repository, None)

        result = await use_case.get_contractor(999)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_contractor_is_called(
        self, 
        use_case: UserQueryUseCaseFacade, 
        user_repository: UserRepository
    ):
        await use_case.get_contractor(1)

        user_repository.get_contractor.assert_awaited_once_with(1)