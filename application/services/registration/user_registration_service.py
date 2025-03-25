from domain.services.registration import UserRegistrationService

from domain.dto.input.registration import UserRegistrationDTO
from domain.dto.common import UserDTO

from domain.repositories import UserRepository
from application.transactions import TransactionManager
from application.external.notification import AdminNotificationService

from domain.entities.enums import UserStatusEnum

from .base_user_modification_service import U, BaseUserModificationService

class BaseUserRegistrationService(UserRegistrationService, BaseUserModificationService):
    """Базовый класс для сервисов регистрации пользователя."""

    async def register_user(self, user_input: UserRegistrationDTO) -> UserDTO:
        return await self._modify_user(user_input)
    
    async def _post_modification_hook(self, user: U):
        await self._post_registration_hook(user)

    async def _post_registration_hook(self, user: U):
        """Переопределение этого метода добавил дополнительные действия после регистрации пользователя"""
        pass

class TelegramUserRegistrationService(BaseUserRegistrationService):
    """
    Реализация интерфейса `UserRegistrationService` для регистрации пользователей из Telegram.
    
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

    def _assign_status(self, user: U) -> U:
        user.status = UserStatusEnum.pending
        return user

    async def _post_registration_hook(self, user: U):
        await self.notification_service.send_new_registration_notification()
        
class WebUserRegistrationService(BaseUserRegistrationService):
    """
    Реализация интерфейса `UserRegistrationService` для регистрации пользователей из Web.
    
    Attributes:
        user_repository (`UserRepository`)
        transaction_manager (`TransactionManager`)
    """

    def _assign_status(self, user: U) -> U:
        user.status = UserStatusEnum.created
        return user