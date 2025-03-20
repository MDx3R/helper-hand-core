from domain.services.registration import ContractorRegistrationService
from application.dtos.input import ContractorInputDTO
from application.dtos.output import ContractorOutputDTO

from domain.entities import Contractor, User
from domain.entities.enums import RoleEnum, UserStatusEnum

from domain.repositories import UserRepository
from domain.exceptions.service import AlreadyAuthenticatedException, UserBlockedException
from domain.services.domain import UserDomainService

from application.external.notification import AdminNotificationService
from application.transactions import TransactionManager, transactional

class ContractorRegistrationServiceImpl(ContractorRegistrationService):
    """
    Класс реализации интерфейса `ContractorRegistrationService` для регистрации исполнителя.
    
    Attributes:
        user_repository (`UserRepository`): Репозиторий с данными пользователей.
        transaction_manager (`TransactionManager`): Менеджер транзакций.
        notification_service (`AdminNotificationService`): Сервис для отправки уведомлений администраторам.
    """

    def __init__(self, user_repository: UserRepository, transaction_manager: TransactionManager, notification_service: AdminNotificationService):
        self.user_repository = user_repository
        self.transaction_manager = transaction_manager
        self.notification_service = notification_service

    async def register_user(self, user_input: ContractorInputDTO) -> ContractorOutputDTO:
        # объявляем транзакцию
        async with self.transaction_manager:
            await self._get_user_and_check_access(user_input.telegram_id)

            contractor = await self._save_contractor(user_input.to_contractor())

        await self._notify_admin(contractor)
        
        return ContractorOutputDTO.from_contractor(contractor)
    
    async def _get_user_and_check_access(self, telegram_id: int) -> User | None:
        """
        Получает объект пользователя по его телеграм ID и проверяет может ли пользователь пройти регистрацию.
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

    async def _save_contractor(self, contractor: Contractor) -> Contractor:
        return await self.user_repository.save_contractor(contractor)
    
    async def _notify_admin(self, contractor: Contractor):
        admins = await self.user_repository.get_admins()
        await self.notification_service.send_new_contractor_registration_notification(admins, contractor)