import pytest

from domain.dto.internal import UserManagementDTO

from tests.unit.services.user.admin.conftest import (
    AdminUserApprovalServiceImpl,
    UserContextDTO,
    UserDTO,
    UserFactory,
    setup_approval_mocks,
    RegistrationApprovedNotificationDTO,
    RegistrationDisapprovedNotificationDTO,
    generate_user_test_case
)

class TestAdminUserApprovalServiceImpl:
    @pytest.fixture
    def service(
        self, 
        approve_user_use_case, 
        disapprove_user_use_case, 
        notification_service
    ):
        return AdminUserApprovalServiceImpl(
            approve_user_use_case=approve_user_use_case,
            disapprove_user_use_case=disapprove_user_use_case,
            notification_service=notification_service
        )

    @pytest.mark.asyncio
    async def test_approve_registration_success(
        self,
        service: AdminUserApprovalServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_approval_mocks(service, user=expected)

        result = await service.approve_registration(
            UserManagementDTO(
                user_id=user.user_id,
                context=context
            )
        )

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_disapprove_registration_success(
        self,
        service: AdminUserApprovalServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_approval_mocks(service, user=expected)

        result = await service.disapprove_registration(
            UserManagementDTO(
                user_id=user.user_id,
                context=context
            )
        )

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_approve_registration_notification_is_called(
        self,
        service: AdminUserApprovalServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_approval_mocks(service, user=expected)

        await service.approve_registration(
            UserManagementDTO(
                user_id=user.user_id,
                context=context
            )
        )

        service.approve_user_use_case.approve_user.assert_awaited_once()
        service.notification_service.send_registration_approved_notification.assert_awaited_once_with(
            RegistrationApprovedNotificationDTO(
                receiver_id=user.user_id, 
                executor_id=context.user_id
            )
        )

    @pytest.mark.asyncio
    async def test_disapprove_registration_notification_is_called(
        self,
        service: AdminUserApprovalServiceImpl,
        context: UserContextDTO
    ):
        user, _ = generate_user_test_case(UserFactory, UserDTO)
        setup_approval_mocks(service, user=user)

        await service.disapprove_registration(
            UserManagementDTO(
                user_id=user.user_id,
                context=context
            )
        )

        service.disapprove_user_use_case.disapprove_user.assert_awaited_once()
        service.notification_service.send_registration_disapproved_notification.assert_awaited_once_with(
            RegistrationDisapprovedNotificationDTO(
                receiver_id=user.user_id, 
                executor_id=context.user_id
            )
        )