from abc import ABC, abstractmethod
from typing import List

from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_filter_dto import (
    ContracteeFilterDTO,
)
from domain.entities.user.contractee.composite_contractee import (
    CompleteContractee,
)
from domain.entities.user.contractee.contractee import Contractee


class ContracteeQueryRepository(ABC):
    @abstractmethod
    async def get_contractee(self, query: UserIdDTO) -> Contractee | None:
        pass

    @abstractmethod
    async def get_complete_contractee(
        self, query: UserIdDTO
    ) -> CompleteContractee | None:
        pass

    @abstractmethod
    async def filter_contractees(
        self, query: ContracteeFilterDTO
    ) -> List[Contractee]:
        pass
