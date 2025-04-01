import pytest
from unittest.mock import AsyncMock
from domain.dto.input.registration import ContractorResetDTO
from domain.dto.context import UserContextDTO
from domain.dto.common import ContractorDTO
from domain.entities.enums import UserStatusEnum
from domain.exceptions.service import PermissionDeniedException
from application.services.registration import ContractorResetService

from .conftest import (
    contractor_test_cases,
    ContractorResetTestCaseGenerator as generator
)

class TestUserResetService:
    @pytest.fixture
    def use_case(self):
        mock = AsyncMock()
        async def reset_contractor(contractor: ContractorResetDTO) -> ContractorDTO:
            data = contractor.get_fields() | {
                "status": UserStatusEnum.pending
            }
            
            return ContractorDTO.model_validate(data)
        
        mock.reset_contractor.side_effect = reset_contractor
        return mock

    @pytest.fixture
    def reset_service(self, use_case, notification_service):
        return ContractorResetService(
            use_case=use_case,
            notification_service=notification_service
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, user_context, expected_user", contractor_test_cases)
    async def test_reset_contractor_is_successful(
        self, 
        reset_service: ContractorResetService, 
        user_input: ContractorResetDTO, 
        user_context: UserContextDTO,
        expected_user: ContractorDTO
    ):
        result = await reset_service.reset_user(user_input, user_context)

        assert isinstance(result, type(expected_user))
        assert result.user_id is not None
        assert result.status == UserStatusEnum.pending
        assert isinstance(result.user_id, int)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, user_context, expected_user", contractor_test_cases)
    async def test_reset_contractor_result_is_correct(
        self, 
        reset_service: ContractorResetService, 
        user_input: ContractorResetDTO, 
        user_context: UserContextDTO,
        expected_user: ContractorDTO
    ):
        result = await reset_service.reset_user(user_input, user_context)

        assert result == expected_user

    @pytest.mark.asyncio
    async def test_reset_contractor_raises_permission_denied(
        self, 
        reset_service: ContractorResetService, 
    ):
        test_case = generator.create_different_id()

        with pytest.raises(PermissionDeniedException) as exc_info:
            await reset_service.reset_user(test_case.input, test_case.context)

        exc = exc_info.value
        assert exc.user_id == test_case.context.user_id
        assert str(test_case.input.user_id) in exc.message

        reset_service.notification_service.send_new_registration_notification.assert_not_awaited()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_input, user_context, expected_user", contractor_test_cases)
    async def test_reset_contractor_has_no_excessive_calls(
        self, 
        reset_service: ContractorResetService, 
        user_input: ContractorResetDTO, 
        user_context: UserContextDTO,
        expected_user: ContractorDTO
    ):
        await reset_service.reset_user(user_input, user_context)

        reset_service.use_case.reset_contractor.assert_awaited_once_with(user_input)
        reset_service.notification_service.send_new_registration_notification.assert_awaited_once()