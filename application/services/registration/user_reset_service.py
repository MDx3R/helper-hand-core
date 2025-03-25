from domain.services.registration import UserResetService

from domain.dto.input.registration import UserResetDTO
from domain.dto.common import UserDTO
from domain.dto.context import UserContextDTO

from domain.repositories import UserRepository
from domain.entities.enums import UserStatusEnum

from application.transactions import TransactionManager
from application.external.notification import AdminNotificationService

from domain.exceptions.service import PermissionDeniedException, UnauthorizedAccessException


from .base_user_modification_service import U, BaseUserModificationService

class UserResetServiceImpl(UserResetService, BaseUserModificationService):
    """
    Класс реализации интерфейса `UserResetService`.
    
    Attributes:
        user_repository (`UserRepository`)
        transaction_manager (`TransactionManager`)
        notification_service (`AdminNotificationService`): Сервис для отправки уведомлений администраторам.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        transaction_manager: TransactionManager,
        notification_service: AdminNotificationService,
    ):
        super().__init__(user_repository, transaction_manager)
        self.notification_service = notification_service

    async def reset_user(self, user_input: UserResetDTO, user: UserContextDTO) -> UserDTO:
        if user_input.user_id != user.user_id:
            raise PermissionDeniedException(
                f"Прохождение повторной регистрации для чужого профиля с id {user_input.user_id} недопустимо", 
                user.user_id
            )
        return await self._modify_user(user_input, user.user_id)
    
    def _assign_status(self, user: U) -> U:
        user.status = UserStatusEnum.created
        return user
    
    async def _post_modification_hook(self, user: U):
        await self.notification_service.send_new_registration_notification()
