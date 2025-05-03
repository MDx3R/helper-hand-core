from abc import ABC, abstractmethod

from domain.services.auth import UserResetService

from domain.dto.input.registration import (
    UserResetDTO,
    ContracteeResetDTO,
    ContractorResetDTO,
)
from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO
from domain.dto.context import UserContextDTO
from domain.dto.internal import ResetDTO
from domain.exceptions.service import PermissionDeniedException

from application.usecases.user import (
    ResetContracteeUseCase,
    ResetContractorUseCase,
)
from application.external.notification import AdminNotificationService


class BaseUserResetService(UserResetService, ABC):
    """Базовый класс для сервисов сброса пользователя."""

    def __init__(
        self,
        notification_service: AdminNotificationService,
    ):
        self.notification_service = notification_service

    async def reset_user(
        self, request: ResetDTO
    ) -> ContracteeDTO | ContractorDTO:
        user_input = request.user
        context = request.context

        if user_input.user_id != context.user_id:
            raise PermissionDeniedException(
                f"Сброс пользователя {user_input.user_id}", context.user_id
            )

        user = await self._reset_user(user_input, context)
        await self._post_reset_hook(user)

        return user

    @abstractmethod
    async def _reset_user(
        self, user_input: UserResetDTO, context: UserContextDTO
    ) -> UserDTO:
        pass

    async def _post_reset_hook(self, user: UserDTO):
        await self.notification_service.send_new_registration_notification()


class ContracteeResetService(BaseUserResetService):
    """
    Класс реализации интерфейса `UserResetService`.

    Attributes:
        use_case (`ResetContracteeUseCase`): Use Case сброса исполнителей.
        notification_service (`AdminNotificationService`): Сервис для отправки уведомлений администраторам.
    """

    def __init__(
        self,
        use_case: ResetContracteeUseCase,
        notification_service: AdminNotificationService,
    ):
        super().__init__(notification_service)
        self.use_case = use_case

    async def _reset_user(
        self, user_input: ContracteeResetDTO, context: UserContextDTO
    ) -> ContracteeDTO:
        return await self.use_case.reset_contractee(user_input)


class ContractorResetService(BaseUserResetService):
    """
    Класс реализации интерфейса `UserResetService`.

    Attributes:
        use_case (`ResetContractorUseCase`): Use Case сброса исполнителей.
        notification_service (`AdminNotificationService`): Сервис для отправки уведомлений администраторам.
    """

    def __init__(
        self,
        use_case: ResetContractorUseCase,
        notification_service: AdminNotificationService,
    ):
        super().__init__(notification_service)
        self.use_case = use_case

    async def _reset_user(
        self, user_input: ContractorResetDTO, context: UserContextDTO
    ) -> ContractorDTO:
        return await self.use_case.reset_contractor(user_input)
