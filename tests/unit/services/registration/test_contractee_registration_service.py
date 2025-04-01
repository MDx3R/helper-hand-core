import pytest
from unittest.mock import AsyncMock
from domain.dto.input.registration import (
    WebContracteeRegistrationDTO, 
    ContracteeRegistrationDTO,
)
from domain.dto.common import ContracteeDTO
from domain.entities.enums import UserStatusEnum
from application.services.registration import (
    WebContracteeRegistrationService, 
    TelegramContracteeRegistrationService
)
from .conftest import (
    telegram_contractee_test_cases,
    web_contractee_test_cases,
    set_up_counter,
    get_counter
)

class TestTelegramContracteeRegistrationService:
    @pytest.fixture
    def use_case(self):
        mock = AsyncMock()
        async def register_contractee(contractee: WebContracteeRegistrationDTO) -> ContracteeDTO:
            counter = get_counter()
            data = contractee.get_fields() | {
                "user_id": counter,
                "status": UserStatusEnum.pending
            }
            set_up_counter(counter + 1)
            
            return ContracteeDTO.model_validate(data)
        
        mock.register_contractee.side_effect = register_contractee
        return mock

    @pytest.fixture
    def registration_service(self, use_case, notification_service):
        return TelegramContracteeRegistrationService(
            use_case=use_case,
            notification_service=notification_service
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", telegram_contractee_test_cases)
    async def test_register_contractee_is_successful(
        self, 
        registration_service: TelegramContracteeRegistrationService, 
        user_input: ContracteeRegistrationDTO, 
        expected_user: ContracteeDTO
    ):
        result = await registration_service.register_user(user_input)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.pending
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", telegram_contractee_test_cases)
    async def test_register_contractee_result_is_correct(
        self, 
        registration_service: TelegramContracteeRegistrationService, 
        user_input: ContracteeRegistrationDTO, 
        expected_user: ContracteeDTO
    ):
        set_up_counter(expected_user.user_id)
        result = await registration_service.register_user(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", telegram_contractee_test_cases)
    async def test_register_contractee_has_no_excessive_calls(
        self, 
        registration_service: TelegramContracteeRegistrationService, 
        user_input: ContracteeRegistrationDTO, 
        expected_user: ContracteeDTO
    ):
        await registration_service.register_user(user_input)

        registration_service.use_case.register_contractee.assert_awaited_once_with(user_input)
        registration_service.notification_service.send_new_registration_notification.assert_awaited_once()

class TestWebContracteeRegistrationService:
    @pytest.fixture
    def use_case(self):
        mock = AsyncMock()
        async def register_contractee(contractee: WebContracteeRegistrationDTO) -> ContracteeDTO:
            counter = get_counter()
            data = contractee.get_fields() | {
                "user_id": counter,
                "status": UserStatusEnum.created
            }
            set_up_counter(counter + 1)
            
            return ContracteeDTO.model_validate(data)
        
        mock.register_contractee.side_effect = register_contractee
        return mock

    @pytest.fixture
    def registration_service(self, use_case):
        return WebContracteeRegistrationService(
            use_case=use_case,
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", web_contractee_test_cases)
    async def test_register_contractee_is_successful(
        self, 
        registration_service: WebContracteeRegistrationService, 
        user_input: ContracteeRegistrationDTO, 
        expected_user: ContracteeDTO
    ):
        result = await registration_service.register_user(user_input)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.created
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", web_contractee_test_cases)
    async def test_register_contractee_result_is_correct(
        self, 
        registration_service: WebContracteeRegistrationService, 
        user_input: ContracteeRegistrationDTO, 
        expected_user: ContracteeDTO
    ):
        set_up_counter(expected_user.user_id)
        result = await registration_service.register_user(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", web_contractee_test_cases)
    async def test_register_contractee_has_no_excessive_calls(
        self, 
        registration_service: WebContracteeRegistrationService, 
        user_input: ContracteeRegistrationDTO, 
        expected_user: ContracteeDTO
    ):
        await registration_service.register_user(user_input)

        registration_service.use_case.register_contractee.assert_awaited_once_with(user_input)