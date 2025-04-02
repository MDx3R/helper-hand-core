import pytest
from unittest.mock import AsyncMock

from domain.dto.common import ContractorDTO, ContracteeDTO
from domain.dto.context import UserContextDTO
from domain.dto.internal import GetUserDTO, GetUserWithContextDTO

from application.usecases.user import GetContracteeUseCase, GetContractorUseCase
from application.services.user import ContractorUserQueryServiceImpl

from tests.factories import AdminFactory, ContracteeFactory, ContractorFactory, ModelBaseFactory

# Настройка моков для ContractorUserQueryServiceImpl
def setup_contractor_query_mocks(
    service: ContractorUserQueryServiceImpl,
    user=None
):
    service.get_contractor_use_case.get_contractor.return_value = user
    service.get_contractee_use_case.get_contractee.return_value = user
    return service

@pytest.fixture
def get_contractee_use_case():
    return AsyncMock(spec=GetContracteeUseCase)

@pytest.fixture
def get_contractor_use_case():
    return AsyncMock(spec=GetContractorUseCase)

@pytest.fixture
def context():
    return UserContextDTO.model_validate(AdminFactory.get_random_data())

def generate_user_test_case(factory: type[ModelBaseFactory], dto: type[ContracteeDTO | ContractorDTO]) -> ContracteeDTO | ContractorDTO:
    expected_dto = dto.from_model(factory.create_model())
    return expected_dto

# Тестовые данные для методов с ролями
contractee_test_data = [
    generate_user_test_case(ContracteeFactory, ContracteeDTO),
]

contractor_test_data = [
    generate_user_test_case(ContractorFactory, ContractorDTO),
]

class TestContractorUserQueryServiceImpl:
    @pytest.fixture
    def service(self, get_contractee_use_case, get_contractor_use_case):
        return ContractorUserQueryServiceImpl(
            get_contractee_use_case=get_contractee_use_case,
            get_contractor_use_case=get_contractor_use_case
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("expected", contractor_test_data)
    async def test_get_profile_success(
        self,
        service: ContractorUserQueryServiceImpl,
        context: UserContextDTO,
        expected
    ):
        setup_contractor_query_mocks(service, user=expected)

        result = await service.get_profile(context)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_profile_not_found(
        self,
        service: ContractorUserQueryServiceImpl,
        context: UserContextDTO
    ):
        setup_contractor_query_mocks(service, user=None)

        result = await service.get_profile(context)

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("expected", contractor_test_data)
    async def test_get_user_self_success(
        self,
        service: ContractorUserQueryServiceImpl,
        context: UserContextDTO,
        expected
    ):
        setup_contractor_query_mocks(service, user=expected)
        user_id = context.user_id
        
        result = await service.get_user(
            GetUserWithContextDTO(
                user_id=user_id,
                context=context
            )
        )

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    @pytest.mark.parametrize("expected", contractee_test_data)
    async def test_get_user_other_success(
        self,
        service: ContractorUserQueryServiceImpl,
        context: UserContextDTO,
        expected
    ):
        different_user_id = context.user_id + 1  # Другой ID, чтобы вызвать get_contractee
        setup_contractor_query_mocks(service, user=expected)

        result = await service.get_user(
            GetUserWithContextDTO(
                user_id=different_user_id,
                context=context
            )
        )

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_user_other_not_found(
        self,
        service: ContractorUserQueryServiceImpl,
        context: UserContextDTO
    ):
        different_user_id = context.user_id + 1  # Другой ID, чтобы вызвать get_contractee
        setup_contractor_query_mocks(service, user=None)

        result = await service.get_user(
            GetUserWithContextDTO(
                user_id=different_user_id,
                context=context
            )
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_get_contractor_use_case_is_called(
        self,
        service: ContractorUserQueryServiceImpl,
        context: UserContextDTO
    ):
        setup_contractor_query_mocks(service)
        await service.get_profile(context)

        service.get_contractor_use_case.get_contractor.assert_awaited_once_with(
            GetUserDTO(
                user_id=context.user_id
            )
        )

    @pytest.mark.asyncio
    async def test_get_contractee_use_case_is_called(
        self,
        service: ContractorUserQueryServiceImpl,
        context: UserContextDTO
    ):
        different_user_id = context.user_id + 1  # Другой ID, чтобы вызвать get_contractee
        setup_contractor_query_mocks(service)
        dto = GetUserWithContextDTO(
            user_id=different_user_id,
            context=context
        )
        await service.get_user(dto)

        service.get_contractee_use_case.get_contractee.assert_awaited_once()