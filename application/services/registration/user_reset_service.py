from domain.services.registration import UserResetService

from domain.dto.input import UserInputDTO, ContracteeInputDTO, ContractorInputDTO
from domain.dto.common import UserDTO
from domain.dto.context import UserContextDTO
from domain.dto.mappers import map_user_to_dto

from domain.repositories import UserRepository
from application.transactions import TransactionManager
from application.external.notification import AdminNotificationService

from domain.entities import User, Contractee, Contractor
from domain.entities.enums import RoleEnum, UserStatusEnum
from domain.exceptions.service import InvalidInputException

from .base_user_modification_service import U, BaseUserModificationService

class UserResetServiceImpl(BaseUserModificationService):
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

    async def reset_user(self, user_input: UserInputDTO, user: UserContextDTO) -> UserDTO:
        return await self._modify_user(user_input, user.user_id)
    
    def _assign_status(self, user: U) -> U:
        user.status = UserStatusEnum.created
        return user
    
    async def _post_modification_hook(self, user: U):
        await self.notification_service.send_new_registration_notification()
