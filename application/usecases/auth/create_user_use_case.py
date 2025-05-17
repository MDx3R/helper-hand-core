from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from application.external.password_hasher import PasswordHasher
from domain.dto.user.request.admin.create_admin_dto import CreateAdminDTO
from domain.dto.user.request.contractee.contractee_registration_dto import (
    CreateContracteeDTO,
)
from domain.dto.user.request.contractor.contractor_registration_dto import (
    CreateContractorDTO,
)
from domain.dto.user.request.create_user_dto import (
    BaseCreateUserDTO,
    CreateCredentialsDTO,
)
from domain.dto.user.response.admin.admin_output_dto import (
    CompleteAdminOutputDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)
from domain.dto.user.response.user_output_dto import (
    BaseCompleteUserOutputDTO,
    UserCredentialsOutputDTO,
)
from domain.entities.user.admin.admin import Admin
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.credentials import (
    TelegramCredentials,
    UserCredentials,
    WebCredentials,
)
from domain.entities.user.user import User
from domain.exceptions.service import InvalidInputException

from application.transactions import transactional

from domain.mappers.user_mappers import (
    AdminMapper,
    ContracteeMapper,
    ContractorMapper,
    TelegramCredentialsMapper,
    UserCredentialsMapper,
    WebCredentialsMapper,
)
from domain.repositories.user.admin.admin_command_repository import (
    AdminCommandRepository,
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


class CreateCredentialsUseCase:
    def __init__(
        self,
        user_command_repository: UserCommandRepository,
        password_hasher: PasswordHasher,
    ):
        self.user_command_repository = user_command_repository
        self.password_hasher = password_hasher

    @transactional
    async def execute(
        self, request: CreateCredentialsDTO
    ) -> UserCredentialsOutputDTO:
        user_id = request.user_id
        credentials = request.credentials

        web = None
        telegram = None
        if credentials.web:
            web = WebCredentialsMapper.from_input(credentials.web, user_id)
            web.password = self.password_hasher.hash(web.password)
            web = await self._create_web_user(web)
        if credentials.telegram:
            telegram = await self._create_telegram_user(
                TelegramCredentialsMapper.from_input(
                    credentials.telegram, user_id
                )
            )

        return UserCredentialsMapper.to_output(
            UserCredentials(telegram=telegram, web=web)
        )

    async def _create_telegram_user(
        self, user: TelegramCredentials
    ) -> TelegramCredentials:
        return await self.user_command_repository.create_telegram_user(user)

    async def _create_web_user(self, user: WebCredentials) -> WebCredentials:
        return await self.user_command_repository.create_web_user(user)


REQUEST = TypeVar("REQUEST", bound=BaseCreateUserDTO)
ROLE = TypeVar("ROLE", bound=User)
OUTPUT = TypeVar("OUTPUT", bound=BaseCompleteUserOutputDTO)


class BaseCreateUserUseCase(ABC, Generic[REQUEST, ROLE, OUTPUT]):
    def __init__(
        self,
        create_credentials_use_case: CreateCredentialsUseCase,
    ):
        self.create_credentials_use_case = create_credentials_use_case

    async def execute(self, request: REQUEST) -> OUTPUT:
        self._validate_request_and_raise_if_invalid(request)
        return await self._create_user(request)

    def _validate_request_and_raise_if_invalid(self, request: REQUEST) -> None:
        if not request.credentials.web and not request.credentials.telegram:
            raise InvalidInputException("Отсутствуют данные аутентификации")

    @transactional
    async def _create_user(self, request: REQUEST) -> OUTPUT:
        user = self._map_to_entity(request)
        user.status = request.status

        user = await self._persist_user(user)
        credentials = await self._create_credentials(user, request)
        return self._build_output(user, credentials)

    async def _create_credentials(
        self, user: User, request: BaseCreateUserDTO
    ) -> UserCredentialsOutputDTO:
        if not user.user_id:
            raise

        credentials = await self.create_credentials_use_case.execute(
            CreateCredentialsDTO(
                credentials=request.credentials,
                user_id=user.user_id,
            )
        )
        return credentials

    @abstractmethod
    def _map_to_entity(self, request: REQUEST) -> ROLE:
        pass

    @abstractmethod
    def _build_output(
        self, user: ROLE, credentials: UserCredentialsOutputDTO
    ) -> OUTPUT:
        pass

    @abstractmethod
    async def _persist_user(self, user: ROLE) -> ROLE:
        pass


class CreateContractorUseCase(
    BaseCreateUserUseCase[
        CreateContractorDTO, Contractor, CompleteContractorOutputDTO
    ]
):
    def __init__(
        self,
        create_credentials_use_case: CreateCredentialsUseCase,
        contractor_command_repository: ContractorCommandRepository,
    ):
        super().__init__(create_credentials_use_case)
        self.contractor_command_repository = contractor_command_repository

    def _map_to_entity(self, request: CreateContractorDTO) -> Contractor:
        return ContractorMapper.from_input(request.user)

    def _build_output(
        self, user: Contractor, credentials: UserCredentialsOutputDTO
    ) -> CompleteContractorOutputDTO:
        return CompleteContractorOutputDTO(
            user=ContractorMapper.to_output(user), credentials=credentials
        )

    async def _persist_user(self, user: Contractor) -> Contractor:
        return await self.contractor_command_repository.create_contractor(user)


class CreateContracteeUseCase(
    BaseCreateUserUseCase[
        CreateContracteeDTO, Contractee, CompleteContracteeOutputDTO
    ]
):
    def __init__(
        self,
        create_credentials_use_case: CreateCredentialsUseCase,
        contractee_command_repository: ContracteeCommandRepository,
    ):
        super().__init__(create_credentials_use_case)
        self.contractee_command_repository = contractee_command_repository

    def _map_to_entity(self, request: CreateContracteeDTO) -> Contractee:
        return ContracteeMapper.from_input(request.user)

    def _build_output(
        self, user: Contractee, credentials: UserCredentialsOutputDTO
    ) -> CompleteContracteeOutputDTO:
        return CompleteContracteeOutputDTO(
            user=ContracteeMapper.to_output(user), credentials=credentials
        )

    async def _persist_user(self, user: Contractee) -> Contractee:
        return await self.contractee_command_repository.create_contractee(user)


class CreateAdminUseCase(
    BaseCreateUserUseCase[CreateAdminDTO, Admin, CompleteAdminOutputDTO]
):
    """Только для внутреннего пользования"""

    def __init__(
        self,
        create_credentials_use_case: CreateCredentialsUseCase,
        admin_command_repository: AdminCommandRepository,
    ):
        super().__init__(create_credentials_use_case)
        self.admin_command_repository = admin_command_repository

    def _map_to_entity(self, request: CreateAdminDTO) -> Admin:
        return AdminMapper.from_input(request.user)

    def _build_output(
        self, user: Admin, credentials: UserCredentialsOutputDTO
    ) -> CompleteAdminOutputDTO:
        return CompleteAdminOutputDTO(
            user=AdminMapper.to_output(user), credentials=credentials
        )

    async def _persist_user(self, user: Admin) -> Admin:
        return await self.admin_command_repository.create_admin(user)
