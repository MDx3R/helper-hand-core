from domain.services.registration import ContracteeRegistrationService
from domain.dto.input import ContracteeInputDTO
from domain.dto.output import ContracteeOutputDTO

from domain.entities import Contractee, User
from domain.entities.enums import RoleEnum, UserStatusEnum

from domain.repositories import UserRepository
from domain.exceptions.service import AlreadyAuthenticatedException, UserBlockedException
from domain.services.domain import UserDomainService

from application.external.notification import AdminNotificationService
from application.transactions import TransactionManager, transactional

class ContracteeRegistrationServiceImpl(ContracteeRegistrationService):
    """
    Класс реализации интерфейса `ContracteeRegistrationService` для регистрации исполнителя.
    
    Attributes:
        user_repository (`UserRepository`): Репозиторий с данными пользователей.
        transaction_manager (`TransactionManager`): Менеджер транзакций.
        notification_service (`AdminNotificationService`): Сервис для отправки уведомлений администраторам.
    """

    def __init__(self, user_repository: UserRepository, transaction_manager: TransactionManager, notification_service: AdminNotificationService):
        self.user_repository = user_repository
        self.transaction_manager = transaction_manager
        self.notification_service = notification_service

    async def register_user(self, user_input: ContracteeInputDTO) -> ContracteeOutputDTO:
        # объявляем транзакцию
        async with self.transaction_manager:
            await self._get_user_and_check_access(user_input.telegram_id)

            contractee = await self._save_contractee(user_input.to_contractee())

        await self._notify_admin(contractee)

        return ContracteeOutputDTO.from_contractee(contractee)

    async def _get_user_and_check_access(self, telegram_id: int) -> User | None:
        """
        Получает объект пользователя и проверяет может ли пользователь пройти регистрацию.
        """
        # note: возможно стоит убрать проверку на авторизации пользователя, так как это делается в контроллере
        user = await self.user_repository.get_user_by_telegram_id(telegram_id)

        if not user:
            return None

        if UserDomainService.is_banned(user):
            raise UserBlockedException("Пользователь заблокирован.")
        elif not UserDomainService.can_be_registered(user):
            raise AlreadyAuthenticatedException("Пользователь уже зарегистрирован.")
        
        return user
    
    async def _save_contractee(self, contractee: Contractee) -> Contractee:
        return await self.user_repository.save_contractee(contractee)

    async def _notify_admin(self, contractee: Contractee):
        admins = await self.user_repository.get_admins()
        await self.notification_service.send_new_contractee_registration_notification(admins, contractee)
