import pytest

from application.usecases.user.user_query_use_case import GetPendingUserUseCase
from domain.dto.user.response.contractee.contractee_output_dto import (
    PendingContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    PendingContractorOutputDTO,
)
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.contractor import Contractor
from domain.repositories.user.user_role_query_repository import (
    UserRoleQueryRepository,
)
from tests.data_generators import (
    ContracteeDataGenerator,
    ContractorDataGenerator,
    UserDataGenerator,
)
from tests.factories import (
    ContracteeFactory,
    ContracteeOutputDTOFactory,
    ContractorFactory,
    ContractorOutputDTOFactory,
)
from .conftest import setup_repository

contractee_gen = ContracteeDataGenerator()
contractor_gen = ContractorDataGenerator()


class TestGetPendingUserUseCase:
    @pytest.mark.asyncio
    async def test_get_pending_contractee_success(
        self,
        use_case: GetPendingUserUseCase,
        user_repository: UserRoleQueryRepository,
    ):
        # Arrange
        contractee = ContracteeFactory(contractee_gen).create_pending()
        expected = ContracteeOutputDTOFactory(contractee_gen).create_pending()

        setup_repository(user_repository, contractee)

        # Act
        result = await use_case.execute()

        # Assert
        assert isinstance(result, PendingContracteeOutputDTO)
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_pending_contractor_success(
        self,
        use_case: GetPendingUserUseCase,
        user_repository: UserRoleQueryRepository,
    ):
        # Arrange
        contractor = ContractorFactory(contractor_gen).create_pending()
        expected = ContractorOutputDTOFactory(contractor_gen).create_pending()

        setup_repository(user_repository, contractor)

        # Act
        result = await use_case.execute()

        # Assert
        assert isinstance(result, PendingContractorOutputDTO)
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_pending_user_not_found(
        self,
        use_case: GetPendingUserUseCase,
        user_repository: UserRoleQueryRepository,
    ):
        setup_repository(user_repository, None)

        result = await use_case.execute()

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "user",
        [
            None,
            ContracteeFactory(contractee_gen).create_pending(),
            ContractorFactory(contractor_gen).create_pending(),
        ],
    )
    async def test_get_pending_user_is_called_properly(
        self,
        use_case: GetPendingUserUseCase,
        user_repository: UserRoleQueryRepository,
        user: Contractee | Contractor,
    ):
        setup_repository(user_repository, user)

        await use_case.execute()

        user_repository.get_first_pending_user.assert_awaited_once()
