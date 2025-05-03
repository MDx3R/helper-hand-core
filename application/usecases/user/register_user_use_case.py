from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from domain.dto.user.request.contractee.contractee_registration_dto import (
    RegisterContracteeDTO,
)
from domain.dto.user.request.contractor.contractor_registration_dto import (
    RegisterContractorDTO,
)
from domain.dto.user.request.user_input_dto import CredentialsInputDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)
from domain.entities.user.contractee.composite_contractee import (
    CompleteContractee,
)
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.composite_contractor import (
    CompleteContractor,
)
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.credentials import (
    TelegramCredentials,
    UserCredentials,
    WebCredentials,
)
from domain.entities.user.enums import UserStatusEnum
from domain.entities.user.user import User
from domain.exceptions.service import InvalidInputException

from application.transactions import transactional

from domain.mappers.user_mappers import (
    ContracteeMapper,
    ContractorMapper,
    TelegramCredentialsMapper,
    WebCredentialsMapper,
)
from domain.repositories.user.contractee.contractee_command_repository import (
    ContracteeCommandRepository,
)
from domain.repositories.user.contractor.contractor_command_repository import (
    ContractorCommandRepository,
)
from domain.repositories.user.user_command_repository import (
    UserCommandRepository,
)


E = TypeVar("E", Contractee, Contractor)
C = TypeVar("C", CompleteContractee, CompleteContractor)
D = TypeVar("D", RegisterContracteeDTO, RegisterContractorDTO)
O = TypeVar("O", CompleteContracteeOutputDTO, CompleteContractorOutputDTO)


class BaseRegisterUserUseCase(ABC, Generic[E, C, D, O]):
    def __init__(self, user_repository: UserCommandRepository):
        self.user_repository = user_repository

    async def execute(self, request: D) -> O:
        self._validate_request_and_raise_if_invalid(request)
        user = await self._register_user(request)
        return self._map_to_output(user)

    def _validate_request_and_raise_if_invalid(self, request: D) -> None:
        if not request.credentials.web and not request.credentials.telegram:
            raise InvalidInputException("Отсутствуют данные аутентификации")
        if request.credentials.web and request.credentials.telegram:
            raise InvalidInputException(
                "Одновременная регистрация с двух ресурсов недопустима"
            )

    @transactional
    async def _register_user(self, request: D) -> C:
        user = self._map_to_entity(request)
        credentials = await self._create_credentials(user, request.credentials)
        user = self._assign_status(user, credentials)
        user = await self._create_entity(user)
        return self._build_complete_entity(user, credentials)

    async def _create_credentials(
        self, user: User, credentials: CredentialsInputDTO
    ) -> UserCredentials:
        web = None
        telegram = None
        if credentials.web:
            web = await self._create_web_user(
                WebCredentialsMapper.from_input(credentials.web, user.user_id)
            )
        if credentials.telegram:
            telegram = await self._create_telegram_user(
                TelegramCredentialsMapper.from_input(
                    credentials.telegram, user.user_id
                )
            )
        return UserCredentials(telegram=telegram, web=web)

    async def _create_telegram_user(
        self, user: TelegramCredentials
    ) -> TelegramCredentials:
        return await self.user_repository.create_telegram_user(user)

    async def _create_web_user(self, user: WebCredentials) -> WebCredentials:
        return await self.user_repository.create_web_user(user)

    @abstractmethod
    def _map_to_entity(self, request: D) -> E:
        pass

    @abstractmethod
    async def _create_entity(self, entity: E) -> E:
        pass

    @abstractmethod
    def _build_complete_entity(
        self, user: E, credentials: UserCredentials
    ) -> C:
        pass

    @abstractmethod
    def _map_to_output(self, user: O) -> O:
        pass

    def _assign_status(self, entity: E, credentials: UserCredentials) -> E:
        entity.status = (
            UserStatusEnum.pending
            if credentials.telegram
            else UserStatusEnum.created
        )
        return entity


class RegisterContracteeUseCase(
    BaseRegisterUserUseCase[
        Contractee,
        CompleteContractee,
        RegisterContracteeDTO,
        CompleteContracteeOutputDTO,
    ]
):
    def __init__(
        self,
        contractee_repository: ContracteeCommandRepository,
        user_repository: UserCommandRepository,
    ):
        super().__init__(user_repository)
        self.contractee_repository = contractee_repository

    def _map_to_entity(self, request: RegisterContracteeDTO) -> Contractee:
        return ContracteeMapper.from_input(request.user)

    async def _create_entity(self, entity: Contractee) -> Contractee:
        return await self.contractee_repository.create_contractee(entity)

    def _build_complete_entity(
        self, user: Contractee, credentials: UserCredentials
    ) -> CompleteContractee:
        return CompleteContractee(user=user, credentials=credentials)

    def _map_to_output(
        self, user: CompleteContractee
    ) -> CompleteContracteeOutputDTO:
        return ContracteeMapper.to_complete(user)


class RegisterContractorUseCase(
    BaseRegisterUserUseCase[
        Contractor,
        CompleteContractor,
        RegisterContractorDTO,
        CompleteContractorOutputDTO,
    ]
):
    def __init__(
        self,
        contractor_repository: ContractorCommandRepository,
        user_repository: UserCommandRepository,
    ):
        super().__init__(user_repository)
        self.contractor_repository = contractor_repository

    def _map_to_entity(self, request: RegisterContractorDTO) -> Contractor:
        return ContractorMapper.from_input(request.user)

    async def _create_entity(self, entity: Contractor) -> Contractor:
        return await self.contractor_repository.create_contractor(entity)

    def _build_complete_entity(
        self, user: Contractor, credentials: UserCredentials
    ) -> CompleteContractor:
        return CompleteContractor(user=user, credentials=credentials)

    def _map_to_output(
        self, user: CompleteContractor
    ) -> CompleteContractorOutputDTO:
        return ContractorMapper.to_complete(user)
