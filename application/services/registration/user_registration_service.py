from abc import ABC, abstractmethod

from domain.services.registration import UserRegistrationService

from domain.dto.input.registration import (
    UserRegistrationDTO,
    ContracteeRegistrationDTO,
    ContractorRegistrationDTO
)
from domain.dto.common import (
    UserDTO,
    ContracteeDTO,
    ContractorDTO
)

from application.usecases.user import (
    RegisterContracteeFromTelegramUseCase,
    RegisterContractorFromTelegramUseCase,
    RegisterContracteeFromWebUseCase,
    RegisterContractorFromWebUseCase
)
from application.external.notification import AdminNotificationService

from domain.dto.mappers import map_user_to_dto

class BaseUserRegistrationService(ABC, UserRegistrationService):
    """Базовый класс для сервисов регистрации пользователя."""

    async def register_user(self, user_input: UserRegistrationDTO) -> UserDTO:
        user = self._register_user(user_input)
        await self._post_registration_hook(user)

        return map_user_to_dto(user)
    
    @abstractmethod
    async def _register_user(self, user_input: UserRegistrationDTO) -> UserDTO:
        pass
    
    @abstractmethod
    async def _post_registration_hook(self, user: UserDTO):
        pass


class TelegramRegistrationMixin:
    """Миксин для сервисов регистрации пользователя из Telegram."""

    def __init__(
        self,
        notification_service: AdminNotificationService
    ):
        self.notification_service = notification_service

    async def _post_registration_hook(self, user: UserDTO):
        await self.notification_service.send_new_registration_notification()


class WebRegistrationMixin:
    """Базовый класс для сервисов регистрации пользователя из Web."""

    async def _post_registration_hook(self, user: UserDTO):
        pass


class ContracteeRegistrationMixin:
    """Миксин для сервисов регистрации исполнителя."""

    def __init__(
        self,
        use_case: RegisterContracteeFromTelegramUseCase | RegisterContracteeFromWebUseCase,
    ):
        self.use_case = use_case

    async def _register_user(self, user_input: ContracteeRegistrationDTO) -> ContracteeDTO:
        return await self.use_case.register_contractee(user_input)


class ContractorRegistrationMixin:
    """Миксин для сервисов регистрации заказчика."""

    def __init__(
        self,
        use_case: RegisterContractorFromTelegramUseCase | RegisterContractorFromWebUseCase,
    ):
        self.use_case = use_case

    async def _register_user(self, user_input: ContractorRegistrationDTO) -> ContractorDTO:
        return await self.use_case.register_contractor(user_input)


class TelegramContracteeRegistrationService(BaseUserRegistrationService, TelegramRegistrationMixin, ContracteeRegistrationMixin):
    """
    Реализация интерфейса `UserRegistrationService` для регистрации исполнителей из Telegram.
    
    Attributes:
        use_case (`RegisterContracteeFromTelegramUseCase`): Use Case регистрации исполнителей.
        notification_service (`AdminNotificationService`): Сервис для отправки уведомлений администраторам.
    """

    def __init__(
        self,
        use_case: RegisterContracteeFromTelegramUseCase,
        notification_service: AdminNotificationService,
    ):
        self.use_case = use_case
        self.notification_service = notification_service


class WebContracteeRegistrationService(BaseUserRegistrationService, WebRegistrationMixin, ContracteeRegistrationMixin):
    """
    Реализация интерфейса `UserRegistrationService` для регистрации исполнителей из Web.
    
    Attributes:
        use_case (`RegisterContracteeFromWebUseCase`): Use Case регистрации исполнителей.
        notification_service (`AdminNotificationService`): Сервис для отправки уведомлений администраторам.
    """

    def __init__(
        self,
        use_case: RegisterContracteeFromWebUseCase,
        notification_service: AdminNotificationService,
    ):
        self.use_case = use_case
        self.notification_service = notification_service


class TelegramContractorRegistrationService(BaseUserRegistrationService, TelegramRegistrationMixin, ContractorRegistrationMixin):
    """
    Реализация интерфейса `UserRegistrationService` для регистрации заказчиков из Telegram.
    
    Attributes:
        use_case (`RegisterContractorFromTelegramUseCase`): Use Case регистрации заказчиков.
    """
    pass


class WebContractorRegistrationService(BaseUserRegistrationService, WebRegistrationMixin, ContractorRegistrationMixin):
    """
    Реализация интерфейса `UserRegistrationService` для регистрации заказчиков из Web.
    
    Attributes:
        use_case (`RegisterContractorFromWebUseCase`): Use Case регистрации заказчиков.
    """
    pass