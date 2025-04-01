import pytest
from unittest.mock import AsyncMock
from domain.dto.input.registration import (
    WebContractorRegistrationDTO, 
    ContractorRegistrationDTO,
)
from domain.dto.common import ContractorDTO
from domain.entities.enums import UserStatusEnum
from application.services.registration import (
    WebContractorRegistrationService, 
    TelegramContractorRegistrationService
)
from .conftest import (
    telegram_contractor_test_cases,
    web_contractor_test_cases,
    set_up_counter,
    get_counter
)

class TestTelegramContractorRegistrationService:
    @pytest.fixture
    def use_case(self):
        mock = AsyncMock()
        async def register_contractor(contractor: WebContractorRegistrationDTO) -> ContractorDTO:
            counter = get_counter()
            data = contractor.get_fields() | {
                "user_id": counter,
                "status": UserStatusEnum.pending
            }
            set_up_counter(counter + 1)
            
            return ContractorDTO.model_validate(data)
        
        mock.register_contractor.side_effect = register_contractor
        return mock

    @pytest.fixture
    def registration_service(self, use_case, notification_service):
        return TelegramContractorRegistrationService(
            use_case=use_case,
            notification_service=notification_service
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", telegram_contractor_test_cases)
    async def test_register_contractor_is_successful(
        self, 
        registration_service: TelegramContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        result = await registration_service.register_user(user_input)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.pending
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", telegram_contractor_test_cases)
    async def test_register_contractor_result_is_correct(
        self, 
        registration_service: TelegramContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        set_up_counter(expected_user.user_id)
        result = await registration_service.register_user(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", telegram_contractor_test_cases)
    async def test_register_contractor_has_no_excessive_calls(
        self, 
        registration_service: TelegramContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        await registration_service.register_user(user_input)

        registration_service.use_case.register_contractor.assert_awaited_once_with(user_input)
        registration_service.notification_service.send_new_registration_notification.assert_awaited_once()

class TestWebContractorRegistrationService:
    @pytest.fixture
    def use_case(self):
        mock = AsyncMock()
        async def register_contractor(contractor: WebContractorRegistrationDTO) -> ContractorDTO:
            counter = get_counter()
            data = contractor.get_fields() | {
                "user_id": counter,
                "status": UserStatusEnum.created
            }
            set_up_counter(counter + 1)
            
            return ContractorDTO.model_validate(data)
        
        mock.register_contractor.side_effect = register_contractor
        return mock

    @pytest.fixture
    def registration_service(self, use_case):
        return WebContractorRegistrationService(
            use_case=use_case,
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", web_contractor_test_cases)
    async def test_register_contractor_is_successful(
        self, 
        registration_service: WebContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        result = await registration_service.register_user(user_input)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.created
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", web_contractor_test_cases)
    async def test_register_contractor_result_is_correct(
        self, 
        registration_service: WebContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        set_up_counter(expected_user.user_id)
        result = await registration_service.register_user(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", web_contractor_test_cases)
    async def test_register_contractor_has_no_excessive_calls(
        self, 
        registration_service: WebContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        await registration_service.register_user(user_input)

        registration_service.use_case.register_contractor.assert_awaited_once_with(user_input)