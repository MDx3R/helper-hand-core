from application.dto.notification.user_status_change import (
    RegistrationApprovedNotificationDTO,
    RegistrationDisapprovedNotificationDTO,
    UserBannedNotificationDTO,
    UserDroppedNotificationDTO,
)
from application.external.notification.notification_service import (
    UserNotificationService,
)
from application.usecases.user.chage_user_status_use_case import (
    ApproveUserUseCase,
    BanUserUseCase,
    DisapproveUserUseCase,
    DropUserUseCase,
)
from application.usecases.user.user_query_use_case import GetPendingUserUseCase
from domain.dto.order.internal.order_managment_dto import DisapproveOrderDTO
from domain.dto.user.internal.user_managment_dto import (
    ApproveUserDTO,
    BanUserDTO,
    DropUserDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)
from domain.dto.user.response.user_output_dto import UserOutputDTO
from domain.services.user.admin_user_service import (
    AdminUserManagementService,
    AdminUserQueryService,
)


class AdminUserQueryServiceImpl(AdminUserQueryService):
    def __init__(self, get_pending_user_use_case: GetPendingUserUseCase):
        self.get_pending_user_use_case = get_pending_user_use_case

    async def get_pending_user(
        self,
    ) -> CompleteContracteeOutputDTO | CompleteContractorOutputDTO | None:
        return await self.get_pending_user_use_case.execute()


class AdminUserManagementServiceImpl(AdminUserManagementService):
    def __init__(
        self,
        approve_user_use_case: ApproveUserUseCase,
        disapprove_user_use_case: DisapproveUserUseCase,
        drop_user_use_case: DropUserUseCase,
        ban_user_use_case: BanUserUseCase,
        notification_service: UserNotificationService,
    ):
        self.approve_user_use_case = approve_user_use_case
        self.disapprove_user_use_case = disapprove_user_use_case
        self.drop_user_use_case = drop_user_use_case
        self.ban_user_use_case = ban_user_use_case

        self.notification_service = notification_service

    async def approve_user(self, request: ApproveUserDTO) -> UserOutputDTO:
        user = await self.approve_user_use_case.execute(request)
        await self.notification_service.send_registration_approved_notification(
            RegistrationApprovedNotificationDTO(
                receiver_id=user.user_id, executor_id=request.context.user_id
            )
        )
        return user

    async def disapprove_registration(
        self, request: DisapproveOrderDTO
    ) -> UserOutputDTO:
        user = await self.approve_user_use_case.execute(request)
        await self.notification_service.send_registration_disapproved_notification(
            RegistrationDisapprovedNotificationDTO(
                receiver_id=user.user_id, executor_id=request.context.user_id
            )
        )
        return user

    async def drop_user(self, request: DropUserDTO) -> UserOutputDTO:
        user = await self.drop_user_use_case.execute(request)
        await self.notification_service.send_user_dropped_notification(
            UserDroppedNotificationDTO(
                receiver_id=user.user_id, executor_id=request.context.user_id
            )
        )
        return user

    async def ban_user(self, request: BanUserDTO) -> UserOutputDTO:
        user = await self.ban_user_use_case.execute(request)
        await self.notification_service.send_user_banned_notification(
            UserBannedNotificationDTO(
                receiver_id=user.user_id, executor_id=request.context.user_id
            )
        )
        return user
