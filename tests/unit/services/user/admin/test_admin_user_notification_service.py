import pytest

from domain.dto.internal import UserNotificationDTO

from tests.unit.services.user.admin.conftest import (
    AdminUserNotificationServiceImpl,
    UserContextDTO,
    setup_notification_mocks,
    AdminContactNotificationDTO
)

class TestAdminUserNotificationServiceImpl:
    @pytest.fixture
    def service(self, notification_service):
        return AdminUserNotificationServiceImpl(notification_service=notification_service)

    @pytest.mark.asyncio
    async def test_notify_user_success(
        self,
        service: AdminUserNotificationServiceImpl,
        context: UserContextDTO
    ):
        user_id = 1
        setup_notification_mocks(service)
        result = await service.notify_user(
            UserNotificationDTO(
                user_id=user_id,
                context=context
            )
        )

        # Здесь нет возвращаемого значения для проверки
        assert result is None

    @pytest.mark.asyncio
    async def test_notify_user_is_called(
        self,
        service: AdminUserNotificationServiceImpl,
        context: UserContextDTO
    ):
        user_id = 1
        setup_notification_mocks(service)
        await service.notify_user(
            UserNotificationDTO(
                user_id=user_id,
                context=context
            )
        )

        service.notification_service.send_admin_contact_notification.assert_awaited_once_with(
            AdminContactNotificationDTO(
                receiver_id=user_id, 
                executor_id=context.user_id
            )
        )