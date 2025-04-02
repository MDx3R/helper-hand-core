import pytest

from domain.dto.internal import UserManagementDTO

from tests.unit.services.user.admin.conftest import (
    AdminUserManagementServiceImpl,
    UserContextDTO,
    UserDTO,
    UserFactory,
    setup_management_mocks,
    UserDroppedNotificationDTO,
    UserBannedNotificationDTO,
    generate_user_test_case
)

class TestAdminUserManagementServiceImpl:
    @pytest.fixture
    def service(
        self, 
        drop_user_use_case, 
        ban_user_use_case, 
        notification_service
    ):
        return AdminUserManagementServiceImpl(
            drop_user_use_case=drop_user_use_case,
            ban_user_use_case=ban_user_use_case,
            notification_service=notification_service
        )

    @pytest.mark.asyncio
    async def test_drop_user_success(
        self,
        service: AdminUserManagementServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_management_mocks(service, user=expected)

        result = await service.drop_user(
            UserManagementDTO(
                user_id=user.user_id,
                context=context
            )
        )

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_ban_user_success(
        self,
        service: AdminUserManagementServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_management_mocks(service, user=expected)

        result = await service.ban_user(
            UserManagementDTO(
                user_id=user.user_id,
                context=context
            )
        )

        assert isinstance(result, type(expected))
        assert result == expected

    @pytest.mark.asyncio
    async def test_drop_user_calls(
        self,
        service: AdminUserManagementServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_management_mocks(service, user=expected)

        await service.drop_user(
            UserManagementDTO(
                user_id=user.user_id,
                context=context
            )
        )

        service.drop_user_use_case.drop_user.assert_awaited_once()
        service.notification_service.send_user_dropped_notification.assert_awaited_once_with(
            UserDroppedNotificationDTO(
                receiver_id=user.user_id, 
                executor_id=context.user_id
            )
        )

    @pytest.mark.asyncio
    async def test_ban_user_calls(
        self,
        service: AdminUserManagementServiceImpl,
        context: UserContextDTO
    ):
        user, expected = generate_user_test_case(UserFactory, UserDTO)
        setup_management_mocks(service, user=expected)

        await service.ban_user(
            UserManagementDTO(
                user_id=user.user_id,
                context=context
            )
        )

        service.ban_user_use_case.ban_user.assert_awaited_once()
        service.notification_service.send_user_banned_notification.assert_awaited_once_with(
            UserBannedNotificationDTO(
                receiver_id=user.user_id, 
                executor_id=context.user_id
            )
        )