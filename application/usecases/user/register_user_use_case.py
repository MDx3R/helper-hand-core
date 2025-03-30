from typing import Literal

from domain.dto.input.registration import (
    UserRegistrationDTO,
    TelegramUserRegistrationDTO,
    WebUserRegistrationDTO,
    WebContracteeRegistrationDTO, 
    TelegramContracteeRegistrationDTO, 
    WebContractorRegistrationDTO,
    TelegramContractorRegistrationDTO,
    ContracteeRegistrationDTO,
    ContractorRegistrationDTO
)

from domain.entities import Contractee, Contractor, TelegramUser
from domain.entities.enums import UserStatusEnum
from domain.dto.common import ContracteeDTO, ContractorDTO
from domain.repositories import UserRepository
from domain.exceptions.service import InvalidInputException

from application.transactions import transactional

from abc import ABC, abstractmethod

from domain.dto.mappers import map_user_to_dto

class RegisterContracteeFromWebUseCase(ABC):
    @abstractmethod
    async def register_contractee(
        self, 
        contractee_input: WebContracteeRegistrationDTO
    ) -> ContracteeDTO:
        pass


class RegisterContracteeFromTelegramUseCase(ABC):
    @abstractmethod
    async def register_contractee(
        self, 
        contractee_input: TelegramContractorRegistrationDTO
    ) -> ContracteeDTO:
        pass


class RegisterContractorFromWebUseCase(ABC):
    @abstractmethod
    async def register_contractor(
        self, 
        contractor_input: WebContractorRegistrationDTO
    ) -> ContractorDTO:
        pass


class RegisterContractorFromTelegramUseCase(ABC):
    @abstractmethod
    async def register_contractor(
        self, 
        contractor_input: TelegramContractorRegistrationDTO
    ) -> ContractorDTO:
        pass


class RegisterUserUseCaseFacade(
    RegisterContracteeFromWebUseCase,
    RegisterContracteeFromTelegramUseCase,
    RegisterContractorFromWebUseCase,
    RegisterContractorFromTelegramUseCase
):
    def __init__(
        self, user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def register_contractee(
        self, 
        contractee_input: WebContracteeRegistrationDTO | TelegramContracteeRegistrationDTO
    ) -> ContracteeDTO:
        return await self.register_user(contractee_input)

    async def register_contractor(
        self,
        contractor_input: WebContractorRegistrationDTO | TelegramContractorRegistrationDTO
    ) -> ContractorDTO:
        return await self.register_user(contractor_input)

    @transactional
    async def register_user(
        self, 
        user_input: UserRegistrationDTO,
    ) -> ContracteeDTO | ContracteeDTO:
        if isinstance(user_input, ContracteeRegistrationDTO):
            user = user_input.to_contractee()
        elif isinstance(user_input, ContractorRegistrationDTO):
            user = user_input.to_contractor()
        else:
            raise InvalidInputException(f"Неподходящий тип {type(user_input).__name__} для DTO пользователя")

        if isinstance(user_input, WebUserRegistrationDTO):
            user = self._assign_status(user, "web")
        elif isinstance(user_input, TelegramUserRegistrationDTO):
            user = self._assign_status(user, "telegram")
        else:
            raise InvalidInputException(f"Неподходящий тип {type(user_input).__name__} для DTO источника пользователя")

        user = await self._create_user(user)

        if isinstance(user_input, TelegramUserRegistrationDTO):
            await self._create_telegram_user(user_input.to_telegram_user(user.user_id))

        return map_user_to_dto(user)

    def _assign_status(
        self, 
        user: Contractee | Contractor, 
        source: Literal["telegram", "web"]
    ) -> Contractee | Contractor:
        if source == "telegram":
            user.status = UserStatusEnum.pending
        elif source == "web":
            user.status = UserStatusEnum.created
        else:
            raise

        return user

    async def _create_user(
        self,
        user: Contractee | Contractor
    ) -> Contractee | Contractor:
        return await self.user_repository.save(user)
    
    async def _create_telegram_user(
        self,
        user: TelegramUser
    ) -> TelegramUser:
        return await self.user_repository.save_telegram_user(user)