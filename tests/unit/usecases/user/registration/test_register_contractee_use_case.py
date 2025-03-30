import pytest

from domain.dto.input.registration import ContracteeRegistrationDTO
from domain.dto.common import UserDTO

from application.usecases.user import (
    RegisterUserUseCaseFacade,
    RegisterContracteeFromWebUseCase,
    RegisterContracteeFromTelegramUseCase
)

from domain.exceptions.service import InvalidInputException

from .generators import (
    UserRegistrationTestCaseGenerator,
    ContracteeRegistrationFromTelegramTestCaseGenerator,
    ContracteeRegistrationFromWebTestCaseGenerator,
)

from ..conftest import set_up_counter

def generate_register_user_test_cases(generator: type[UserRegistrationTestCaseGenerator]):
    return [
        generator.create(),
    ]

def generate_contractee_telegram_test_cases():
    return [(t.input, t.expected) for t in generate_register_user_test_cases(ContracteeRegistrationFromTelegramTestCaseGenerator)]

def generate_contractee_web_test_cases():
    return [(t.input, t.expected) for t in generate_register_user_test_cases(ContracteeRegistrationFromWebTestCaseGenerator)]

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
def web_contractee_input():
    return ContracteeRegistrationFromWebTestCaseGenerator.create().input

@pytest.fixture
def telegram_contractee_input():
    return ContracteeRegistrationFromTelegramTestCaseGenerator.create().input

class TestWebRegisterContracteeFromWebUseCase:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractee_web_test_cases())
    async def test_register_contractee_is_successful(
        self, 
        web_use_case: RegisterContracteeFromWebUseCase,
        user_input: ContracteeRegistrationDTO, 
        expected_user: UserDTO
    ):
        result = await web_use_case.register_contractee(user_input)
        
        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert isinstance(result.user_id, int)
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractee_web_test_cases())
    async def test_register_contractee_result_is_correct(
        self, 
        web_use_case: RegisterContracteeFromWebUseCase,
        user_input: ContracteeRegistrationDTO, 
        expected_user: UserDTO
    ):
        set_up_counter(expected_user.user_id)
        result = await web_use_case.register_contractee(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    async def test_register_contractee_raises_when_invalid_input(
        self, 
        web_use_case: RegisterContracteeFromWebUseCase,
        invalid_input
    ):
        with pytest.raises(InvalidInputException) as exc_info:
            await web_use_case.register_contractee(invalid_input)

    @pytest.mark.asyncio
    async def test_register_contractee_has_no_excessive_calls(
        self, 
        web_use_case: RegisterUserUseCaseFacade,
        web_contractee_input: ContracteeRegistrationDTO
    ):
        await web_use_case.register_contractee(web_contractee_input)

        web_use_case.user_repository.save.assert_awaited_once()
        web_use_case.user_repository.save_telegram_user.assert_not_awaited()

class TestTelegramRegisterContracteeFromWebUseCase:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractee_telegram_test_cases())
    async def test_register_contractee_is_successful(
        self, 
        telegram_use_case: RegisterContracteeFromTelegramUseCase,
        user_input: ContracteeRegistrationDTO, 
        expected_user: UserDTO
    ):
        result = await telegram_use_case.register_contractee(user_input)
        
        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert isinstance(result.user_id, int)
    
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractee_telegram_test_cases())
    async def test_register_contractee_result_is_correct(
        self, 
        telegram_use_case: RegisterContracteeFromTelegramUseCase,
        user_input: ContracteeRegistrationDTO, 
        expected_user: UserDTO
    ):
        set_up_counter(expected_user.user_id)
        result = await telegram_use_case.register_contractee(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    async def test_register_contractee_raises_when_invalid_input(
        self, 
        telegram_use_case: RegisterContracteeFromTelegramUseCase,
        invalid_input
    ):
        with pytest.raises(InvalidInputException) as exc_info:
            await telegram_use_case.register_contractee(invalid_input)

    @pytest.mark.asyncio
    async def test_register_contractee_has_no_excessive_calls(
        self, 
        web_use_case: RegisterUserUseCaseFacade,
        telegram_contractee_input: ContracteeRegistrationDTO
    ):
        await web_use_case.register_contractee(telegram_contractee_input)

        web_use_case.user_repository.save.assert_awaited_once()
        web_use_case.user_repository.save_telegram_user.assert_awaited_once()