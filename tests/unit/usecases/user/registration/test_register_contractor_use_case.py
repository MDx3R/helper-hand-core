import pytest
from domain.dto.input.registration import ContractorRegistrationDTO
from domain.dto.common import UserDTO
from application.usecases.user import (
    RegisterUserUseCaseFacade,
    RegisterContractorFromWebUseCase,
    RegisterContractorFromTelegramUseCase
)
from domain.exceptions.service import InvalidInputException

from .conftest import (
    contractor_web_test_cases,
    contractor_telegram_test_cases,
)
from ..conftest import set_up_counter

class TestWebRegisterContractorFromWebUseCase:
    @pytest.fixture
    def web_use_case(self, user_repository):
        service = RegisterUserUseCaseFacade(
            user_repository=user_repository,
        )
        return service

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", contractor_web_test_cases)
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
    @pytest.mark.parametrize("user_input, expected_user", contractor_web_test_cases)
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
        web_use_case: RegisterUserUseCaseFacade,
        invalid_input
    ):
        with pytest.raises(InvalidInputException) as exc_info:
            await web_use_case.register_contractor(invalid_input)

        web_use_case.user_repository.save.assert_not_awaited()
        web_use_case.user_repository.save_telegram_user.assert_not_awaited()

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
    @pytest.fixture
    def telegram_use_case(self, user_repository):
        service = RegisterUserUseCaseFacade(
            user_repository=user_repository,
        )
        return service

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", contractor_telegram_test_cases)
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
    @pytest.mark.parametrize("user_input, expected_user", contractor_telegram_test_cases)
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
        telegram_use_case: RegisterUserUseCaseFacade,
        invalid_input
    ):
        with pytest.raises(InvalidInputException) as exc_info:
            await telegram_use_case.register_contractor(invalid_input)

        telegram_use_case.user_repository.save.assert_not_awaited()
        telegram_use_case.user_repository.save_telegram_user.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_register_contractor_has_no_excessive_calls(
        self, 
        telegram_use_case: RegisterUserUseCaseFacade,
        telegram_contractor_input: ContractorRegistrationDTO
    ):
        await telegram_use_case.register_contractor(telegram_contractor_input)

        telegram_use_case.user_repository.save.assert_awaited_once()
        telegram_use_case.user_repository.save_telegram_user.assert_awaited_once()