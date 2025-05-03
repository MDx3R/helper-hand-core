from typing import Generic, TypeVar
from domain.dto.user.request.contractee.contractee_registration_dto import (
    ResetContracteeDTO,
)
from domain.dto.user.request.contractor.contractor_registration_dto import (
    ResetContractorDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
)
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.enums import UserStatusEnum

from application.transactions import transactional

from abc import ABC, abstractmethod

from domain.mappers.user_mappers import ContracteeMapper, ContractorMapper
from domain.repositories.user.contractee.contractee_command_repository import (
    ContracteeCommandRepository,
)
from domain.repositories.user.contractor.contractor_command_repository import (
    ContractorCommandRepository,
)


E = TypeVar("E", Contractee, Contractor)
D = TypeVar("D", ResetContracteeDTO, ResetContractorDTO)
O = TypeVar("O", ContracteeOutputDTO, ContractorOutputDTO)


class ResetUserUseCase(ABC, Generic[E, D, O]):
    @transactional
    async def execute(self, request: D) -> O:
        user = self._map_to_entity(request)
        user.user_id = request.context.user_id
        user = await self._reset_user(user)
        return self._map_to_output(user)

    async def _reset_user(self, user: E) -> E:
        user.status = UserStatusEnum.pending
        return await self._save_user(user)

    @abstractmethod
    def _map_to_entity(self, request: D) -> E:
        pass

    @abstractmethod
    def _map_to_output(self, user: E) -> O:
        pass

    @abstractmethod
    async def _save_user(self, user: E) -> E:
        pass


class ResetContracteeUseCase(
    ResetUserUseCase[
        Contractee,
        ResetContracteeDTO,
        ContracteeOutputDTO,
    ]
):
    def __init__(
        self,
        repository: ContracteeCommandRepository,
    ):
        self.repository = repository

    def _map_to_entity(self, request: ResetContracteeDTO) -> Contractee:
        return ContracteeMapper.from_input(request.user)

    def _map_to_output(self, user: Contractee) -> ContracteeOutputDTO:
        return ContracteeMapper.to_output(user)

    async def _save_user(self, user: Contractee) -> Contractee:
        return await self.repository.update_contractee(user)


class ResetContractorUseCase(
    ResetUserUseCase[
        Contractor,
        ResetContractorDTO,
        ContractorOutputDTO,
    ]
):
    def __init__(
        self,
        repository: ContractorCommandRepository,
    ):
        self.repository = repository

    def _map_to_entity(self, request: ResetContractorDTO) -> Contractor:
        return ContractorMapper.from_input(request.user)

    def _map_to_output(self, user: Contractor) -> ContractorOutputDTO:
        return ContractorMapper.to_output(user)

    async def _save_user(self, user: Contractor) -> Contractor:
        return await self.repository.update_contractor(user)
