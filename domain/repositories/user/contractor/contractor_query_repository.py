from abc import ABC, abstractmethod
from typing import List

from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_filter_dto import (
    ContractorFilterDTO,
)
from domain.entities.user.contractor.composite_contractor import (
    CompleteContractor,
)
from domain.entities.user.contractor.contractor import Contractor


class ContractorQueryRepository(ABC):
    @abstractmethod
    async def get_contractor(self, query: UserIdDTO) -> Contractor | None:
        pass

    @abstractmethod
    async def get_complete_contractor(
        self, query: UserIdDTO
    ) -> CompleteContractor | None:
        pass

    @abstractmethod
    async def filter_contractors(
        self, query: ContractorFilterDTO
    ) -> List[Contractor]:
        pass
