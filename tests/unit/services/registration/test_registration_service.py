import pytest
from unittest.mock import AsyncMock, Mock

from domain.dto.input.registration import UserRegistrationDTO
from domain.dto.common import UserDTO

from domain.entities import User, Contractee, Contractor
from domain.entities.enums import UserStatusEnum, RoleEnum

from application.services.registration import TelegramUserRegistrationService, WebUserRegistrationService

from .generators import (
    TelegramContracteeRegistrationTestCaseGenerator, 
    WebContracteeRegistrationTestCaseGenerator,
    TelegramContractorRegistrationTestCaseGenerator,
    WebContractorRegistrationTestCaseGenerator
)

counter = 1

@pytest.fixture
def user_repository():
    mock = AsyncMock()

    async def save(user: Contractee | Contractor) -> Contractee | Contractor:
        global counter
        data = user.get_fields()
        if not user.user_id:
            role_id_field = "contractee_id" if user.role == RoleEnum.contractee else "contractor_id"
            data = data | {
                "user_id": counter, 
                role_id_field: counter
            }
        
        counter +=1

        return user.model_validate(data)
        
    mock.save.side_effect = save
    return mock

@pytest.fixture
def transaction_manager():
    mock = AsyncMock()

    mock.__aenter__ = AsyncMock(return_value=None)
    mock.__aexit__ = AsyncMock(return_value=None)
    return mock

@pytest.fixture
def notification_service():
    mock = AsyncMock()
    mock.send_new_registration_notification = AsyncMock(return_value=None)
    return mock

@pytest.fixture
def telegram_registration_service(user_repository, transaction_manager, notification_service):
    service = TelegramUserRegistrationService(
        user_repository=user_repository,
        transaction_manager=transaction_manager,
        notification_service=notification_service
    )
    return service

@pytest.fixture
def web_registration_service(user_repository, transaction_manager):
    service = WebUserRegistrationService(
        user_repository=user_repository,
        transaction_manager=transaction_manager,
    )
    return service

def set_up_counter(user_id: int):
        global counter
        counter = user_id

def generate_successful_contractee_registration_test_case(telegram: bool = False):
    if telegram:
        test_case = TelegramContracteeRegistrationTestCaseGenerator.create_successful(random=True)
    else:
        test_case = WebContracteeRegistrationTestCaseGenerator.create_successful(random=True)

    return (test_case.input, test_case.expected)

def generate_successful_contractor_registration_test_case(telegram: bool = False):
    if telegram:
        test_case = TelegramContractorRegistrationTestCaseGenerator.create_successful(random=True)
    else:
        test_case = WebContractorRegistrationTestCaseGenerator.create_successful(random=True)

    return (test_case.input, test_case.expected)

successful_web_user_registration_data = [
    generate_successful_contractee_registration_test_case(),
    generate_successful_contractor_registration_test_case()
]
successful_telegram_user_registration_data = [
    generate_successful_contractee_registration_test_case(telegram=True),
    generate_successful_contractor_registration_test_case(telegram=True)
]

class TestTelegramUserRegistrationService:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", successful_telegram_user_registration_data)
    async def test_register_user_is_successful(
        self, 
        telegram_registration_service: TelegramUserRegistrationService, 
        user_input: UserRegistrationDTO, 
        expected_user: UserDTO
    ):
        result = await telegram_registration_service.register_user(user_input)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.pending
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", successful_telegram_user_registration_data)
    async def test_register_user_has_no_excessive_calls(
        self, 
        telegram_registration_service: TelegramUserRegistrationService, 
        user_input: UserRegistrationDTO, 
        expected_user: UserDTO
    ):
        result = await telegram_registration_service.register_user(user_input)

        telegram_registration_service.user_repository.save.assert_awaited_once()
        telegram_registration_service.notification_service.send_new_registration_notification.assert_awaited_once()
        telegram_registration_service.transaction_manager.__aenter__.assert_awaited_once()
        telegram_registration_service.transaction_manager.__aexit__.assert_awaited_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", successful_telegram_user_registration_data)
    async def test_register_user_result_is_correct(
        self, 
        telegram_registration_service: TelegramUserRegistrationService, 
        user_input: UserRegistrationDTO, 
        expected_user: UserDTO
    ):
        set_up_counter(expected_user.user_id)

        result = await telegram_registration_service.register_user(user_input)

        assert result == expected_user


class TestWebContracteeRegistrationService:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", successful_web_user_registration_data)
    async def test_register_user_is_successful(
        self, 
        web_registration_service: WebUserRegistrationService,
        user_input: UserRegistrationDTO, 
        expected_user: UserDTO
    ):
        result = await web_registration_service.register_user(user_input)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.created
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", successful_web_user_registration_data)
    async def test_register_user_has_no_excessive_calls(
        self, 
        web_registration_service: WebUserRegistrationService,
        user_input: UserRegistrationDTO, 
        expected_user: UserDTO
    ):
        result = await web_registration_service.register_user(user_input)

        web_registration_service.user_repository.save.assert_awaited_once()
        web_registration_service.transaction_manager.__aenter__.assert_awaited_once()
        web_registration_service.transaction_manager.__aexit__.assert_awaited_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, expected_user", successful_web_user_registration_data)
    async def test_register_user_result_is_correct(
        self, 
        web_registration_service: WebUserRegistrationService,
        user_input: UserRegistrationDTO, 
        expected_user: UserDTO
    ):
        set_up_counter(expected_user.user_id)

        result = await web_registration_service.register_user(user_input)

        assert result == expected_user