from domain.dto.input.registration import (
    UserResetDTO,
    ContracteeResetDTO,
    ContractorResetDTO
)

from domain.entities import Contractee, Contractor
from domain.entities.enums import UserStatusEnum
from domain.dto.common import ContracteeDTO, ContractorDTO
from domain.repositories import UserRepository
from domain.exceptions.service import InvalidInputException

from application.transactions import transactional

from abc import ABC, abstractmethod

from domain.dto.mappers import map_user_to_dto

class ResetContracteeUseCase(ABC):
    @abstractmethod
    async def reset_contractee(
        self, 
        contractee_input: ContracteeResetDTO
    ) -> ContracteeDTO:
        pass


class ResetContractorUseCase(ABC):
    @abstractmethod
    async def register_contractor(
        self, 
        contractor_input: ContractorResetDTO
    ) -> ContractorDTO:
        pass


class ResetUserUseCaseFacade(
    ResetContracteeUseCase,
    ResetContractorUseCase,
):
    def __init__(
        self, user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def reset_contractee(
        self, 
        contractee_input: ContracteeResetDTO
    ) -> ContracteeDTO:
        return await self.reset_user(contractee_input)

    async def reset_contractor(
        self,
        contractor_input: ContractorResetDTO
    ) -> ContractorDTO:
        return await self.reset_user(contractor_input)

    @transactional
    async def reset_user(
        self, 
        user_input: UserResetDTO,
    ) -> ContracteeDTO | ContracteeDTO:
        if isinstance(user_input, ContracteeResetDTO):
            user = user_input.to_contractee()
        elif isinstance(user_input, ContractorResetDTO):
            user = user_input.to_contractor()
        else:
            raise InvalidInputException(f"Неподходящий тип {type(user_input).__name__} для DTO пользователя")

        user.status = UserStatusEnum.pending
        user = await self._save_user(user)

        return map_user_to_dto(user)

    async def _save_user(
        self,
        user: Contractee | Contractor
    ) -> Contractee | Contractor:
        return await self.user_repository.save(user)