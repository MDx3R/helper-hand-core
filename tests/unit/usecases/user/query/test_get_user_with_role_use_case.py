import pytest

from application.usecases.user.user_query_use_case import (
    GetAdminUseCase,
    GetContracteeUseCase,
    GetContractorUseCase,
    GetUserWithRoleUseCase,
)

from application.usecases.user import UserQueryUseCaseFacade
from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_query_dto import GetUserDTO
from domain.dto.user.response.admin.admin_output_dto import AdminOutputDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
)
from domain.entities.user.admin.admin import Admin
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.contractor import Contractor
from domain.repositories.user.admin.admin_query_repository import (
    AdminQueryRepository,
)
from domain.repositories.user.contractee.contractee_query_repository import (
    ContracteeQueryRepository,
)
from domain.repositories.user.contractor.contractor_query_repository import (
    ContractorQueryRepository,
)
from domain.repositories.user.user_role_query_repository import (
    UserRoleQueryRepository,
)
from tests.data_generators import (
    AdminDataGenerator,
    ContracteeDataGenerator,
    ContractorDataGenerator,
)
from tests.factories import (
    AdminFactory,
    AdminOutputDTOFactory,
    ContracteeFactory,
    ContracteeOutputDTOFactory,
    ContractorFactory,
    ContractorOutputDTOFactory,
)
from .conftest import setup_repository

contractee_gen = ContracteeDataGenerator()
contractor_gen = ContractorDataGenerator()
admin_gen = AdminDataGenerator()

test_cases = [
    (
        AdminOutputDTO,
        AdminFactory(admin_gen).create_default(),
        AdminOutputDTOFactory(admin_gen).create(),
    ),
    (
        ContractorOutputDTO,
        ContractorFactory(contractor_gen).create_default(),
        ContractorOutputDTOFactory(contractor_gen).create(),
    ),
    (
        ContracteeOutputDTO,
        ContracteeFactory(contractee_gen).create_default(),
        ContracteeOutputDTOFactory(contractee_gen).create(),
    ),
    (
        None,
        None,
        None,
    ),
]


class TestGetUserWithRoleUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    @pytest.mark.asyncio
    @pytest.mark.parametrize("output_type, user, expected", test_cases)
    async def test_get_user_with_role(
        self,
        use_case: GetUserWithRoleUseCase,
        user_repository: UserRoleQueryRepository,
        output_type: type[
            AdminOutputDTO | ContractorOutputDTO | ContracteeOutputDTO
        ],
        user: Admin | Contractor | Contractee,
        expected: AdminOutputDTO | ContractorOutputDTO | ContracteeOutputDTO,
    ):
        setup_repository(user_repository, user)

        result = await use_case.execute(GetUserDTO(user_id=user.user_id))

        assert isinstance(result, output_type)
        assert result == expected

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "user",
        [
            None,
            AdminFactory(admin_gen).create_default(),
            ContractorFactory(contractor_gen).create_default(),
            ContracteeFactory(contractee_gen).create_default(),
        ],
    )
    async def test_get_user_with_role_is_called_properly(
        self,
        use_case: GetUserWithRoleUseCase,
        user_repository: UserRoleQueryRepository,
        user: Admin | Contractor | Contractee,
    ):
        user_id = 999 if not user else user.user_id

        await use_case.execute(GetUserDTO(user_id=user_id))

        user_repository.get_user.assert_awaited_once_with(
            UserIdDTO(user_id=user.user_id)
        )


class TestGetAdminUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    async def test_get_admin(
        self,
        use_case: GetAdminUseCase,
        user_repository: AdminQueryRepository,
    ):
        # Arrange
        admin = AdminFactory(admin_gen).create_default()
        expected = AdminOutputDTOFactory(admin_gen).create()

        setup_repository(user_repository, admin)

        # Act
        result = await use_case.exetute(GetUserDTO(user_id=admin.user_id))

        # Assert
        assert isinstance(result, AdminOutputDTO)
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_admin_not_found(
        self,
        use_case: GetAdminUseCase,
        user_repository: AdminQueryRepository,
    ):
        user_id = 999

        setup_repository(user_repository, None)

        result = await use_case.exetute(GetUserDTO(user_id=user_id))

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "user",
        [
            None,
            AdminFactory(admin_gen).create_default(),
        ],
    )
    async def test_get_admin_is_called_properly(
        self,
        use_case: GetAdminUseCase,
        user_repository: AdminQueryRepository,
        user: Admin,
    ):
        user_id = 999 if not user else user.user_id

        setup_repository(user_repository, user)

        await use_case.exetute(GetUserDTO(user_id=user_id))

        user_repository.get_admin.assert_awaited_once_with(
            UserIdDTO(user_id=user_id)
        )


class TestGetContracteeUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    async def test_get_contractee_success(
        self,
        use_case: GetContracteeUseCase,
        user_repository: ContracteeQueryRepository,
    ):
        # Arrange
        contractee = ContracteeFactory(contractee_gen).create_default()
        expected = ContracteeOutputDTOFactory(contractee_gen).create()

        setup_repository(user_repository, contractee)

        # Act
        result = await use_case.execute(GetUserDTO(user_id=contractee.user_id))

        # Assert
        assert isinstance(result, ContracteeOutputDTO)
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_contractee_not_found(
        self,
        use_case: GetContracteeUseCase,
        user_repository: ContracteeQueryRepository,
    ):
        user_id = 999

        setup_repository(user_repository, None)

        result = await use_case.execute(GetUserDTO(user_id=user_id))

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "user",
        [
            None,
            ContracteeFactory(contractee_gen).create_default(),
        ],
    )
    async def test_get_contractee_is_called_properly(
        self,
        use_case: GetContracteeUseCase,
        user_repository: ContracteeQueryRepository,
        user: Contractee,
    ):
        user_id = 999 if not user else user.user_id

        setup_repository(user_repository, user)

        await use_case.execute(GetUserDTO(user_id=user_id))

        user_repository.get_contractee.assert_awaited_once_with(
            UserIdDTO(user_id=user_id)
        )


class TestGetContractorUseCase:
    @pytest.fixture
    def use_case(self, user_repository):
        return UserQueryUseCaseFacade(user_repository)

    @pytest.mark.asyncio
    async def test_get_contractor_success(
        self,
        use_case: GetContractorUseCase,
        user_repository: ContractorQueryRepository,
    ):
        # Arrange
        contractor = ContractorFactory(contractor_gen).create_default()
        expected = ContractorOutputDTOFactory(contractor_gen).create()

        setup_repository(user_repository, contractor)

        # Act
        result = await use_case.execute(GetUserDTO(user_id=contractor.user_id))

        # Assert
        assert isinstance(result, ContractorOutputDTO)
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_contractor_not_found(
        self,
        use_case: GetContractorUseCase,
        user_repository: ContractorQueryRepository,
    ):
        user_id = 999

        setup_repository(user_repository, None)

        result = await use_case.execute(GetUserDTO(user_id=user_id))

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "user",
        [
            None,
            ContractorFactory(contractor_gen).create_default(),
        ],
    )
    async def test_get_contractor_is_called_properly(
        self,
        use_case: GetContractorUseCase,
        user_repository: ContractorQueryRepository,
        user: Contractor,
    ):
        user_id = 999 if not user else user.user_id

        setup_repository(user_repository, user)

        await use_case.execute(GetUserDTO(user_id=user_id))

        user_repository.get_contractor.assert_awaited_once_with(
            UserIdDTO(user_id=user_id)
        )
