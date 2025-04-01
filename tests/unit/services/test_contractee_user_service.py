import pytest
from unittest.mock import AsyncMock

from domain.dto.common import ContracteeDTO
from domain.dto.context import UserContextDTO

from application.usecases.user import GetContracteeUseCase
from application.services.user import ContracteeUserQueryServiceImpl

from tests.factories import AdminFactory, ContracteeFactory, ModelBaseFactory

# Настройка моков для ContracteeUserQueryServiceImpl
def setup_contractee_query_mocks(
    service: ContracteeUserQueryServiceImpl,
    user=None
):
    service.get_contractee_use_case.get_contractee.return_value = user
    return service

@pytest.fixture
def get_contractee_use_case():
    return AsyncMock(spec=GetContracteeUseCase)

@pytest.fixture
def context():
    return UserContextDTO.model_validate(AdminFactory.get_random_data())

def generate_user_test_case(factory: type[ModelBaseFactory], dto: type[ContracteeDTO]) -> ContracteeDTO:
    expected_dto = dto.from_model(factory.create_model())
    return expected_dto

# Тестовые данные для Contractee
contractee_test_data = [
    generate_user_test_case(ContracteeFactory, ContracteeDTO),
]

class TestContracteeUserQueryServiceImpl:
    @pytest.fixture
    def service(self, get_contractee_use_case):
        return ContracteeUserQueryServiceImpl(
            get_contractee_use_case=get_contractee_use_case
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("expected", contractee_test_data)
    async def test_get_profile_success(
        self,
        service: ContracteeUserQueryServiceImpl,
        context: UserContextDTO,
        expected
    ):
        setup_contractee_query_mocks(service, user=expected)

        result = await service.get_profile(context)

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_profile_not_found(
        self,
        service: ContracteeUserQueryServiceImpl,
        context: UserContextDTO
    ):
        setup_contractee_query_mocks(service, user=None)

        result = await service.get_profile(context)

        assert result is None

    @pytest.mark.asyncio
    async def test_get_contractee_use_case_is_called(
        self,
        service: ContracteeUserQueryServiceImpl,
        context: UserContextDTO
    ):
        setup_contractee_query_mocks(service)
        await service.get_profile(context)

        service.get_contractee_use_case.get_contractee.assert_awaited_once_with(context.user_id)