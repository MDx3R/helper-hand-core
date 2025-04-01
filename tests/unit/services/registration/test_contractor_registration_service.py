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

from tests.generators.registration import (
    UserRegistrationTestCaseGenerator,
    ContractorRegistrationFromWebTestCaseGenerator,
    ContractorRegistrationFromTelegramTestCaseGenerator
)

counter = 1

@pytest.fixture
def web_use_case():
    mock = AsyncMock()

    async def register_contractor( 
        contractor: WebContractorRegistrationDTO
    ) -> ContractorDTO:
        global counter
        
        data = contractor.get_fields() | {
            "user_id": counter,
            "status": UserStatusEnum.created
        }

        counter +=1

        return ContractorDTO.model_validate(data)

    mock.register_contractor.side_effect = register_contractor
    return mock

@pytest.fixture
def telegram_use_case():
    mock = AsyncMock()

    async def register_contractor( 
        contractor: WebContractorRegistrationDTO
    ) -> ContractorDTO:
        global counter

        data = contractor.get_fields() | {
            "user_id": counter,
            "status": UserStatusEnum.pending
        }

        counter +=1

        return ContractorDTO.model_validate(data)

    mock.register_contractor.side_effect = register_contractor
    return mock

@pytest.fixture
def notification_service():
    mock = AsyncMock()
    mock.send_new_registration_notification = AsyncMock(return_value=None)
    return mock

@pytest.fixture
def web_registration_service(web_use_case):
    service = WebContractorRegistrationService(
        use_case=web_use_case,
    )
    return service

@pytest.fixture
def telegram_registration_service(telegram_use_case, notification_service):
    service = TelegramContractorRegistrationService(
        use_case=telegram_use_case,
        notification_service=notification_service
    )
    return service

def set_up_counter(user_id: int):
    global counter
    counter = user_id

def generate_register_contractor_test_cases(generator: type[UserRegistrationTestCaseGenerator]):
    return [
        generator.create(),
    ]

def generate_contractor_telegram_test_cases():
    return [(t.input, t.expected) for t in generate_register_contractor_test_cases(ContractorRegistrationFromTelegramTestCaseGenerator)]

def generate_contractor_web_test_cases():
    return [(t.input, t.expected) for t in generate_register_contractor_test_cases(ContractorRegistrationFromWebTestCaseGenerator)]

telegram_test_cases = generate_contractor_telegram_test_cases()
web_test_cases = generate_contractor_web_test_cases()

class TestTelegramContractorRegistrationService:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", telegram_test_cases)
    async def test_register_contractor_is_successful(
        self, 
        telegram_registration_service: TelegramContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        result = await telegram_registration_service.register_user(user_input)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.pending
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", telegram_test_cases)
    async def test_register_contractor_result_is_correct(
        self, 
        telegram_registration_service: TelegramContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        set_up_counter(expected_user.user_id)

        result = await telegram_registration_service.register_user(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", telegram_test_cases)
    async def test_register_contractor_has_no_excessive_calls(
        self, 
        telegram_registration_service: TelegramContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        await telegram_registration_service.register_user(user_input)

        telegram_registration_service.use_case.register_contractor.assert_awaited_once_with(user_input)
        telegram_registration_service.notification_service.send_new_registration_notification.assert_awaited_once()


class TestWebContractorRegistrationService:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", web_test_cases)
    async def test_register_contractor_is_successful(
        self, 
        web_registration_service: WebContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        result = await web_registration_service.register_user(user_input)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.created
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", web_test_cases)
    async def test_register_contractor_result_is_correct(
        self, 
        web_registration_service: WebContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        set_up_counter(expected_user.user_id)

        result = await web_registration_service.register_user(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", web_test_cases)
    async def test_register_contractor_has_no_excessive_calls(
        self, 
        web_registration_service: WebContractorRegistrationService, 
        user_input: ContractorRegistrationDTO, 
        expected_user: ContractorDTO
    ):
        await web_registration_service.register_user(user_input)
        
        web_registration_service.use_case.register_contractor.assert_awaited_once_with(user_input)