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

from tests.generators.registration import (
    UserRegistrationTestCaseGenerator,
    ContracteeRegistrationFromWebTestCaseGenerator,
    ContracteeRegistrationFromTelegramTestCaseGenerator
)

counter = 1

@pytest.fixture
def web_use_case():
    mock = AsyncMock()

    async def register_contractee( 
        contractee: WebContracteeRegistrationDTO
    ) -> ContracteeDTO:
        global counter
        
        data = contractee.get_fields() | {
            "user_id": counter,
            "status": UserStatusEnum.created
        }

        counter +=1

        return ContracteeDTO.model_validate(data)

    mock.register_contractee.side_effect = register_contractee
    return mock

@pytest.fixture
def telegram_use_case():
    mock = AsyncMock()

    async def register_contractee( 
        contractee: WebContracteeRegistrationDTO
    ) -> ContracteeDTO:
        global counter

        data = contractee.get_fields() | {
            "user_id": counter,
            "status": UserStatusEnum.pending
        }

        counter +=1

        return ContracteeDTO.model_validate(data)

    mock.register_contractee.side_effect = register_contractee
    return mock

@pytest.fixture
def notification_service():
    mock = AsyncMock()
    mock.send_new_registration_notification = AsyncMock(return_value=None)
    return mock

@pytest.fixture
def web_registration_service(web_use_case):
    service = WebContracteeRegistrationService(
        use_case=web_use_case,
    )
    return service

@pytest.fixture
def telegram_registration_service(telegram_use_case, notification_service):
    service = TelegramContracteeRegistrationService(
        use_case=telegram_use_case,
        notification_service=notification_service
    )
    return service

def set_up_counter(user_id: int):
    global counter
    counter = user_id

def generate_register_contractee_test_cases(generator: type[UserRegistrationTestCaseGenerator]):
    return [
        generator.create(),
    ]

def generate_contractee_telegram_test_cases():
    return [(t.input, t.expected) for t in generate_register_contractee_test_cases(ContracteeRegistrationFromTelegramTestCaseGenerator)]

def generate_contractee_web_test_cases():
    return [(t.input, t.expected) for t in generate_register_contractee_test_cases(ContracteeRegistrationFromWebTestCaseGenerator)]

class TestTelegramContracteeRegistrationService:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractee_telegram_test_cases())
    async def test_register_contractee_is_successful(
        self, 
        telegram_registration_service: TelegramContracteeRegistrationService, 
        user_input: ContracteeRegistrationDTO, 
        expected_user: ContracteeDTO
    ):
        result = await telegram_registration_service.register_user(user_input)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.pending
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractee_telegram_test_cases())
    async def test_register_contractee_result_is_correct(
        self, 
        telegram_registration_service: TelegramContracteeRegistrationService, 
        user_input: ContracteeRegistrationDTO, 
        expected_user: ContracteeDTO
    ):
        set_up_counter(expected_user.user_id)

        result = await telegram_registration_service.register_user(user_input)

        assert result == expected_user

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractee_telegram_test_cases())
    async def test_register_contractee_has_no_excessive_calls(
        self, 
        telegram_registration_service: TelegramContracteeRegistrationService, 
        user_input: ContracteeRegistrationDTO, 
        expected_user: ContracteeDTO
    ):
        result = await telegram_registration_service.register_user(user_input)

        telegram_registration_service.notification_service.send_new_registration_notification.assert_awaited_once()


class TestWebContracteeRegistrationService:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractee_web_test_cases())
    async def test_register_contractee_is_successful(
        self, 
        web_registration_service: WebContracteeRegistrationService, 
        user_input: ContracteeRegistrationDTO, 
        expected_user: ContracteeDTO
    ):
        result = await web_registration_service.register_user(user_input)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.created
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", generate_contractee_web_test_cases())
    async def test_register_contractee_result_is_correct(
        self, 
        web_registration_service: WebContracteeRegistrationService, 
        user_input: ContracteeRegistrationDTO, 
        expected_user: ContracteeDTO
    ):
        set_up_counter(expected_user.user_id)

        result = await web_registration_service.register_user(user_input)

        assert result == expected_user