from domain.services.user import (
    AdminUserApprovalService,
    AdminUserManagementService,
    AdminUserQueryService,
    AdminUserNotificationService
)

from application.usecases.user import (
    DropUserUseCase,
    BanUserUseCase,
    ApproveUserUseCase,
    DisapproveUserUseCase,
)
from application.dto.notification import (
    RegistrationApprovedNotificationDTO,
    RegistrationDisapprovedNotificationDTO,
    UserDroppedNotificationDTO,
    UserBannedNotificationDTO
)
from application.external.notification import UserNotificationService

from domain.dto.context import UserContextDTO
from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO, AdminDTO

class AdminUserManagementServiceImpl(AdminUserManagementService):
    def __init__(
        self,
        drop_user_use_case: DropUserUseCase,
        ban_user_use_case: BanUserUseCase,
        notification_service: UserNotificationService
    ):
        self.drop_user_use_case = drop_user_use_case
        self.ban_user_use_case = ban_user_use_case
        self.notification_service = notification_service

    async def drop_user(self, user_id: int, context: UserContextDTO) -> UserDTO:
        user = await self.drop_user_use_case.drop_user(user_id)
        await self._notify_dropped_user(user, context)
        return user

    async def ban_user(self, user_id: int, context: UserContextDTO) -> UserDTO:
        user = await self.ban_user_use_case.ban_user(user_id)
        await self._notify_banned_user(user, context)
        return user

    async def _notify_dropped_user(self, user: UserDTO, context: UserContextDTO):
        await self.notification_service.send_user_dropped_notification(
            UserDroppedNotificationDTO(
                receiver_id=user.user_id,
                executor_id=context.user_id
            )
        )

    async def _notify_banned_user(self, user: UserDTO, context: UserContextDTO):
        await self.notification_service.send_user_banned_notification(
            UserBannedNotificationDTO(
                receiver_id=user.user_id,
                executor_id=context.user_id
            )
        )


class AdminUserApprovalServiceImpl(AdminUserApprovalService):
    def __init__(
        self,
        approve_user_use_case: ApproveUserUseCase,
        disapprove_user_use_case: DisapproveUserUseCase,
        notification_service: UserNotificationService
    ):
        self.approve_user_use_case = approve_user_use_case
        self.disapprove_user_use_case = disapprove_user_use_case
        self.notification_service = notification_service

    async def approve_registration(
        self, 
        user_id: int, 
        context: UserContextDTO
    ) -> UserDTO:
        user = await self.approve_user_use_case.approve_user(user_id)
        await self._notify_registration_approved(user, context)
        return user

    async def disapprove_registration(
        self, 
        user_id: int, 
        context: UserContextDTO
    ) -> UserDTO:
        user = await self.disapprove_user_use_case.disapprove_user(user_id)
        await self._notify_registration_disapproved(user, context)
        return user
    
    async def _notify_registration_approved(
        self, 
        user: UserDTO, 
        context: UserContextDTO
    ):
        await self.notification_service.send_registration_approved_notification(
            RegistrationApprovedNotificationDTO(
                receiver_id=user.user_id,
                executor_id=context.user_id
            )
        )

    async def _notify_registration_disapproved(
        self, 
        user: UserDTO, 
        context: UserContextDTO
    ):
        await self.notification_service.send_registration_disapproved_notification(
            RegistrationDisapprovedNotificationDTO(
                receiver_id=user.user_id,
                executor_id=context.user_id
            )
        )

class AdminUserQueryServiceImpl(AdminUserQueryService):
    pass


class AdminUserNotificationServiceImpl(AdminUserNotificationService):
    pass