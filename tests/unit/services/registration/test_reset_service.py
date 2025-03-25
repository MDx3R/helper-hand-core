import pytest
from unittest.mock import AsyncMock, Mock

from domain.dto.input.registration import UserResetDTO
from domain.dto.context import UserContextDTO
from domain.dto.common import UserDTO

from domain.entities import User, Contractee, Contractor
from domain.entities.enums import UserStatusEnum, RoleEnum

from domain.exceptions.service import PermissionDeniedException

from application.services.registration import UserResetServiceImpl

from .generators import (
    UserResetTestCasesGenerator,
    ContracteeResetTestCasesGenerator,
    ContractorResetTestCasesGenerator
)

@pytest.fixture
def user_repository():
    mock = AsyncMock()

    async def save(user: Contractee | Contractor) -> Contractee | Contractor:
        data = user.get_fields()
        
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
def reset_service(user_repository, transaction_manager, notification_service):
    service = UserResetServiceImpl(
        user_repository=user_repository,
        transaction_manager=transaction_manager,
        notification_service=notification_service
    )
    return service

def generate_successful_user_reset_test_case(
    generator: type[UserResetTestCasesGenerator],
    same_user_id: bool = True, 
    same_telegram_id: bool = True, 
    same_chat_id: bool = True
):
    if not same_user_id:
        test_case = generator.create_different_id(random=True)
    elif not same_telegram_id:
        test_case = generator.create_different_telegram_id(random=True)
    elif not same_chat_id:
        test_case = generator.create_different_chat_id(random=True)
    else:
        test_case = generator.create_successful(random=True)

    return (test_case.input, test_case.context, test_case.expected)

def generate_successful_contractee_reset_test_case(
    same_user_id: bool = True, 
    same_telegram_id: bool = True, 
    same_chat_id: bool = True
):
    return generate_successful_user_reset_test_case(
        ContracteeResetTestCasesGenerator,
        same_user_id,
        same_telegram_id,
        same_chat_id,
    )

def generate_successful_contractor_reset_test_case(
    same_user_id: bool = True, 
    same_telegram_id: bool = True, 
    same_chat_id: bool = True
):
    return generate_successful_user_reset_test_case(
        ContractorResetTestCasesGenerator,
        same_user_id,
        same_telegram_id,
        same_chat_id,
    )

successful_user_reset_data = [
    generate_successful_contractee_reset_test_case(),
    generate_successful_contractor_reset_test_case()
]
different_id_user_reset_data = [
    generate_successful_contractee_reset_test_case(same_user_id=False),
    generate_successful_contractee_reset_test_case(same_telegram_id=False),
    generate_successful_contractee_reset_test_case(same_chat_id=False),
    generate_successful_contractor_reset_test_case(same_user_id=False),
    generate_successful_contractor_reset_test_case(same_telegram_id=False),
    generate_successful_contractor_reset_test_case(same_chat_id=False),
]

class TestUserResetService:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, user_context, expected_user", successful_user_reset_data)
    async def test_reset_user_is_successful(
        self, 
        reset_service: UserResetServiceImpl, 
        user_input: UserResetDTO, 
        user_context: UserContextDTO,
        expected_user: UserDTO
    ):
        result = await reset_service.reset_user(user_input, user_context)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.pending
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, user_context, expected_user", successful_user_reset_data)
    async def test_reset_user_has_no_excessive_calls(
        self, 
        reset_service: UserResetServiceImpl, 
        user_input: UserResetDTO, 
        user_context: UserContextDTO,
        expected_user: UserDTO
    ):
        result = await reset_service.reset_user(user_input, user_context)

        reset_service.user_repository.save.assert_awaited_once()
        reset_service.notification_service.send_new_registration_notification.assert_awaited_once()
        reset_service.transaction_manager.__aenter__.assert_awaited_once()
        reset_service.transaction_manager.__aexit__.assert_awaited_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, user_context, expected_user", successful_user_reset_data)
    async def test_reset_user_result_is_correct(
        self, 
        reset_service: UserResetServiceImpl, 
        user_input: UserResetDTO, 
        user_context: UserContextDTO,
        expected_user: UserDTO
    ):
        result = await reset_service.reset_user(user_input, user_context)

        assert result == expected_user

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, user_context, expected_user", different_id_user_reset_data)
    async def test_reset_user_result_is_correct(
        self, 
        reset_service: UserResetServiceImpl, 
        user_input: UserResetDTO, 
        user_context: UserContextDTO,
        expected_user: UserDTO
    ):
        with pytest.raises(PermissionDeniedException) as exc_info:
            await reset_service.reset_user(user_input, user_context)

        exc = exc_info.value
        assert exc.user_id == user_context.user_id
        assert str(user_input.user_id) in exc.message