from domain.models import User, Admin
from domain.models.enums import RoleEnum, UserStatusEnum
from domain.services.user import AdminUserService
from domain.repositories import UserRepository
from domain.exceptions.service import UserStatusChangeNotAllowedException, NotFoundException

from application.transactions import TransactionManager
from application.external.notification import NotificationService
from application.dtos.output import UserOutputDTO, ContracteeOutputDTO, ContractorOutputDTO, AdminOutputDTO
from application.dtos.mappers import map_user_to_dto

class AdminUserServiceImpl(AdminUserService):
    def __init__(
        self, 
        user_repository: UserRepository,
        transaction_manager: TransactionManager,
        user_notification_service: NotificationService,
    ):
        self.user_repository = user_repository
        self.transaction_manager = transaction_manager
        self.user_notification_service = user_notification_service

    def _map_user_to_dto(self, user: User):
        return map_user_to_dto(user)

    async def get_user(self, user_id: int, admin: Admin) -> UserOutputDTO | None:
        user = await self.user_repository.get_user_with_role(user_id)
        if not user:
            return None
        
        return self._map_user_to_dto(user)

    async def get_first_pending_user(self, admin: Admin) -> UserOutputDTO | None:
        user = await self.user_repository.get_first_pending_user_with_role()
        if not user:
            return None
        
        return self._map_user_to_dto(user)

    async def approve_registration(self, user_id: int, admin: Admin) -> UserOutputDTO:
        async with self.transaction_manager:
            user = await self._get_user_with_role_and_check_exists(user_id)
            
            await self._check_user_registration_can_be_approved(user, UserStatusEnum.registered)

            user = await self._change_user_status(user, UserStatusEnum.registered)
        
        await self.user_notification_service.send_registration_approved_notification(user)

        return self._map_user_to_dto(user)

    async def disapprove_registration(self, user_id: int, admin: Admin) -> UserOutputDTO:
        async with self.transaction_manager:
            user = await self._get_user_with_role_and_check_exists(user_id)
            
            await self._check_user_registration_can_be_approved(user, UserStatusEnum.dropped)

            user = await self._change_user_status(user, UserStatusEnum.dropped)
        
        await self.user_notification_service.send_registration_disapproved_notification(user)

        return self._map_user_to_dto(user)

    async def _send_notifications_on_registration_approval(self, user: User):
        if user.status == UserStatusEnum.registered:
            await self._notify_registration_approved(user)
        else:
            await self._notify_registration_disapproved(user)

    async def _notify_registration_approved(self, user: User):
        await self.user_notification_service.send_registration_approved_notification(user)

    async def _notify_registration_disapproved(self, user: User):
        await self.user_notification_service.send_registration_disapproved_notification(user)

    async def drop_user(self, user_id: int, admin: Admin) -> UserOutputDTO:
        async with self.transaction_manager:
            user = await self._get_user_with_role_and_check_exists(user_id)

            await self._check_user_status_can_be_changed(user, UserStatusEnum.dropped)

            user = await self._change_user_status(user, UserStatusEnum.dropped)
        
        await self._notify_dropped_user(user)

        return self._map_user_to_dto(user)

    async def ban_user(self, user_id: int, admin: Admin) -> UserOutputDTO:
        async with self.transaction_manager:
            user = await self._get_user_with_role_and_check_exists(user_id)

            await self._check_user_status_can_be_changed(user, UserStatusEnum.banned)

            user = await self._change_user_status(user, UserStatusEnum.banned)
        
        await self._notify_banned_user(user)

        return self._map_user_to_dto(user)

    async def _notify_dropped_user(self, user: User):
        await self.user_notification_service.send_user_dropped_notification(user)

    async def _notify_banned_user(self, user: User):
        await self.user_notification_service.send_user_banned_notification(user)

    async def _get_user_with_role_and_check_exists(self, user_id: int) -> User:
        user = await self.user_repository.get_user_with_role(user_id)
        if not user:
            return NotFoundException(user_id)
        return user

    async def _check_user_registration_can_be_approved(self, user: User, status: UserStatusEnum):
        if user.status != UserStatusEnum.pending:
            raise UserStatusChangeNotAllowedException(user.user_id, status, "Пользователь не требует подтверждения регистрации")

    async def _check_user_status_can_be_changed(self, user: User, status: UserStatusEnum):
        if user.role == RoleEnum.admin:
            raise UserStatusChangeNotAllowedException(
                user.user_id, status, 
                "Регистрация пользователя не может быть сброшена" if status == UserStatusEnum.dropped
                else "Пользователь не может быть заблокирован" if status == UserStatusEnum.banned else ""
            )

    async def _change_user_status(self, user: User, status: UserStatusEnum) -> User:
        await self.user_repository.change_user_status(user.user_id, status)
        user.status = status
        
        return user

    async def notify_user(self, user_id: int, admin: Admin):
        user = await self.user_repository.get_user_by_id(user_id)
        await self.user_notification_service.send_admin_contact_notification(user, admin)