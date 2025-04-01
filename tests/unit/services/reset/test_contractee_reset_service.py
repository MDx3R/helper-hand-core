import pytest
from unittest.mock import AsyncMock
from domain.dto.input.registration import ContracteeResetDTO
from domain.dto.context import UserContextDTO
from domain.dto.common import ContracteeDTO
from domain.entities.enums import UserStatusEnum
from domain.exceptions.service import PermissionDeniedException
from application.services.registration import ContracteeResetService

from .conftest import (
    contractee_test_cases,
    ContracteeResetTestCaseGenerator as generator
)

class TestUserResetService:
    @pytest.fixture
    def use_case(self):
        mock = AsyncMock()
        async def reset_contractee(contractee: ContracteeResetDTO) -> ContracteeDTO:
            data = contractee.get_fields() | {
                "status": UserStatusEnum.pending
            }
            
            return ContracteeDTO.model_validate(data)
        
        mock.reset_contractee.side_effect = reset_contractee
        return mock

    @pytest.fixture
    def reset_service(self, use_case, notification_service):
        return ContracteeResetService(
            use_case=use_case,
            notification_service=notification_service
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, user_context, expected_user", contractee_test_cases)
    async def test_reset_contractee_is_successful(
        self, 
        reset_service: ContracteeResetService, 
        user_input: ContracteeResetDTO, 
        user_context: UserContextDTO,
        expected_user: ContracteeDTO
    ):
        result = await reset_service.reset_user(user_input, user_context)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.pending
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, user_context, expected_user", contractee_test_cases)
    async def test_reset_contractee_result_is_correct(
        self, 
        reset_service: ContracteeResetService, 
        user_input: ContracteeResetDTO, 
        user_context: UserContextDTO,
        expected_user: ContracteeDTO
    ):
        result = await reset_service.reset_user(user_input, user_context)

        assert result == expected_user

    @pytest.mark.asyncio
    async def test_reset_contractee_raises_permission_denied(
        self, 
        reset_service: ContracteeResetService, 
    ):
        test_case = generator.create_different_id()

        with pytest.raises(PermissionDeniedException) as exc_info:
            await reset_service.reset_user(test_case.input, test_case.context)

        exc = exc_info.value
        assert exc.user_id == test_case.context.user_id
        assert str(test_case.input.user_id) in exc.message

        reset_service.notification_service.send_new_registration_notification.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, user_context, expected_user", contractee_test_cases)
    async def test_reset_contractee_has_no_excessive_calls(
        self, 
        reset_service: ContracteeResetService, 
        user_input: ContracteeResetDTO, 
        user_context: UserContextDTO,
        expected_user: ContracteeDTO
    ):
        await reset_service.reset_user(user_input, user_context)

        reset_service.use_case.reset_contractee.assert_awaited_once_with(user_input)
        reset_service.notification_service.send_new_registration_notification.assert_awaited_once()