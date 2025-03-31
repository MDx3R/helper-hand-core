import pytest

from domain.dto.input.registration import ContractorRegistrationDTO
from domain.dto.common import UserDTO

from application.usecases.user import (
    RegisterUserUseCaseFacade,
    RegisterContractorFromWebUseCase,
    RegisterContractorFromTelegramUseCase
)

from domain.exceptions.service import InvalidInputException

from tests.generators.registration import (
    UserRegistrationTestCaseGenerator,
    ContractorRegistrationFromTelegramTestCaseGenerator,
    ContractorRegistrationFromWebTestCaseGenerator
)

from ..conftest import set_up_counter

def generate_register_user_test_cases(generator: type[UserRegistrationTestCaseGenerator]):
    return [
        generator.create(),
    ]

def generate_contractor_telegram_test_cases():
    return [(t.input, t.expected) for t in generate_register_user_test_cases(ContractorRegistrationFromTelegramTestCaseGenerator)]

def generate_contractor_web_test_cases():
    return [(t.input, t.expected) for t in generate_register_user_test_cases(ContractorRegistrationFromWebTestCaseGenerator)]

@pytest.fixture
def web_use_case(user_repository):
    service = RegisterUserUseCaseFacade(
        user_repository=user_repository,
    )
    return service

@pytest.fixture
def telegram_use_case(user_repository):
    service = RegisterUserUseCaseFacade(
        user_repository=user_repository,
    )
    return service

@pytest.fixture
def invalid_input():
    return UserRegistrationTestCaseGenerator.create_invalid_input().input

@pytest.fixture
def web_contractor_input():
    return ContractorRegistrationFromWebTestCaseGenerator.create().input

@pytest.fixture
def telegram_contractor_input():
    return ContractorRegistrationFromTelegramTestCaseGenerator.create().input

class TestWebRegisterContractorFromWebUseCase:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractor_web_test_cases())
    async def test_register_contractor_is_successful(
        self, 
        web_use_case: RegisterContractorFromWebUseCase,
        user_input: ContractorRegistrationDTO, 
        expected_user: UserDTO
    ):
        result = await web_use_case.register_contractor(user_input)
        
        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert isinstance(result.user_id, int)
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractor_web_test_cases())
    async def test_register_contractor_result_is_correct(
        self, 
        web_use_case: RegisterContractorFromWebUseCase,
        user_input: ContractorRegistrationDTO, 
        expected_user: UserDTO
    ):
        set_up_counter(expected_user.user_id)
        result = await web_use_case.register_contractor(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    async def test_register_contractor_raises_when_invalid_input(
        self, 
        web_use_case: RegisterContractorFromWebUseCase,
        invalid_input
    ):
        with pytest.raises(InvalidInputException) as exc_info:
            await web_use_case.register_contractor(invalid_input)

    @pytest.mark.asyncio
    async def test_register_contractor_has_no_excessive_calls(
        self, 
        web_use_case: RegisterUserUseCaseFacade,
        web_contractor_input: ContractorRegistrationDTO
    ):
        await web_use_case.register_contractor(web_contractor_input)

        web_use_case.user_repository.save.assert_awaited_once()
        web_use_case.user_repository.save_telegram_user.assert_not_awaited()

class TestTelegramRegisterContractorFromWebUseCase:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractor_telegram_test_cases())
    async def test_register_contractor_is_successful(
        self, 
        telegram_use_case: RegisterContractorFromTelegramUseCase,
        user_input: ContractorRegistrationDTO, 
        expected_user: UserDTO
    ):
        result = await telegram_use_case.register_contractor(user_input)
        
        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert isinstance(result.user_id, int)
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractor_telegram_test_cases())
    async def test_register_contractor_result_is_correct(
        self, 
        telegram_use_case: RegisterContractorFromTelegramUseCase,
        user_input: ContractorRegistrationDTO, 
        expected_user: UserDTO
    ):
        set_up_counter(expected_user.user_id)
        result = await telegram_use_case.register_contractor(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    async def test_register_contractor_raises_when_invalid_input(
        self, 
        telegram_use_case: RegisterContractorFromTelegramUseCase,
        invalid_input
    ):
        with pytest.raises(InvalidInputException) as exc_info:
            await telegram_use_case.register_contractor(invalid_input)

    @pytest.mark.asyncio
    async def test_register_contractor_has_no_excessive_calls(
        self, 
        web_use_case: RegisterUserUseCaseFacade,
        telegram_contractor_input: ContractorRegistrationDTO
    ):
        await web_use_case.register_contractor(telegram_contractor_input)

        web_use_case.user_repository.save.assert_awaited_once()
        web_use_case.user_repository.save_telegram_user.assert_awaited_once()