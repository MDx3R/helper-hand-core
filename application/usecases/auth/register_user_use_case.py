from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from application.usecases.auth.create_user_use_case import (
    CreateContracteeUseCase,
    CreateContractorUseCase,
)
from domain.dto.user.base import (
    TelegramCredentialsDTO,
    UserCredentialsDTO,
    WebCredentialsDTO,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.contractee.contractee_registration_dto import (
    CreateContracteeDTO,
    RegisterContracteeDTO,
)
from domain.dto.user.request.contractor.contractor_registration_dto import (
    CreateContractorDTO,
    RegisterContractorDTO,
)
from domain.dto.user.request.user_input_dto import BaseRegisterUserDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
    ContracteeRegistationOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
    ContractorRegistationOutputDTO,
)
from domain.dto.user.response.user_output_dto import (
    AuthOutputDTO,
    BaseUserRegistationOutputDTO,
    UserCredentialsOutputDTO,
    UserOutputDTO,
)

from domain.entities.user.enums import UserStatusEnum
from domain.services.auth.token_service import TokenService


def build_user_context(
    user: UserOutputDTO, credentials: UserCredentialsOutputDTO
) -> UserContextDTO:
    tg = credentials.telegram
    web = credentials.web
    return UserContextDTO(
        user_id=user.user_id,
        role=user.role,
        status=user.status,
        credentials=UserCredentialsDTO(
            telegram=(
                TelegramCredentialsDTO(
                    telegram_id=tg.telegram_id, chat_id=tg.chat_id
                )
                if tg
                else None
            ),
            web=WebCredentialsDTO(email=web.email) if web else None,
        ),
    )


REQUEST = TypeVar("REQUEST", bound=BaseRegisterUserDTO)
OUTPUT = TypeVar("OUTPUT", bound=BaseUserRegistationOutputDTO)
COMPLETE = TypeVar(
    "COMPLETE", CompleteContracteeOutputDTO, CompleteContractorOutputDTO
)


class RegisterUserUseCase(ABC, Generic[REQUEST, COMPLETE, OUTPUT]):
    STATUS_UPON_REGISTRATION: UserStatusEnum

    def __init__(
        self,
        token_service: TokenService,
    ):
        self.token_service = token_service

    async def execute(self, request: REQUEST) -> OUTPUT:
        complete_user = await self._create_user(request)
        token = await self.token_service.generate_token(
            build_user_context(complete_user.user, complete_user.credentials)
        )
        return self._build_output(complete_user, token)

    @abstractmethod
    def _build_output(self, user: COMPLETE, token: AuthOutputDTO) -> OUTPUT:
        pass

    @abstractmethod
    async def _create_user(self, request: REQUEST) -> COMPLETE:
        pass


class RegisterContracteeUseCase(
    RegisterUserUseCase[
        RegisterContracteeDTO,
        CompleteContracteeOutputDTO,
        ContracteeRegistationOutputDTO,
    ]
):
    STATUS_UPON_REGISTRATION: UserStatusEnum = UserStatusEnum.pending

    def __init__(
        self,
        token_service: TokenService,
        create_contractee_use_case: CreateContracteeUseCase,
    ):
        super().__init__(token_service)
        self.create_contractee_use_case = create_contractee_use_case

    def _build_output(
        self, user: CompleteContracteeOutputDTO, token: AuthOutputDTO
    ) -> ContracteeRegistationOutputDTO:
        return ContracteeRegistationOutputDTO(token=token, user=user)

    async def _create_user(
        self, request: RegisterContracteeDTO
    ) -> CompleteContracteeOutputDTO:
        return await self.create_contractee_use_case.execute(
            CreateContracteeDTO(
                credentials=request.credentials,
                status=self.STATUS_UPON_REGISTRATION,
                user=request.user,
            )
        )


class RegisterContractorUseCase(
    RegisterUserUseCase[
        RegisterContractorDTO,
        CompleteContractorOutputDTO,
        ContractorRegistationOutputDTO,
    ]
):
    STATUS_UPON_REGISTRATION: UserStatusEnum = UserStatusEnum.pending

    def __init__(
        self,
        token_service: TokenService,
        create_contractor_use_case: CreateContractorUseCase,
    ):
        super().__init__(token_service)
        self.create_contractor_use_case = create_contractor_use_case

    def _build_output(
        self, user: CompleteContractorOutputDTO, token: AuthOutputDTO
    ) -> ContractorRegistationOutputDTO:
        return ContractorRegistationOutputDTO(token=token, user=user)

    async def _create_user(
        self, request: RegisterContractorDTO
    ) -> CompleteContractorOutputDTO:
        return await self.create_contractor_use_case.execute(
            CreateContractorDTO(
                credentials=request.credentials,
                status=self.STATUS_UPON_REGISTRATION,
                user=request.user,
            )
        )
