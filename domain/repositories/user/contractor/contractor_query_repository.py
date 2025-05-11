from abc import ABC, abstractmethod
from typing import List

from domain.dto.user.internal.user_filter_dto import (
    ContractorFilterDTO,
)
from domain.entities.user.contractor.composite_contractor import (
    CompleteContractor,
)
from domain.entities.user.contractor.contractor import Contractor


class ContractorQueryRepository(ABC):
    @abstractmethod
    async def get_contractor(self, user_id: int) -> Contractor | None:
        pass

    @abstractmethod
    async def get_complete_contractor(
        self, user_id: int
    ) -> CompleteContractor | None:
        pass

    @abstractmethod
    async def filter_contractors(
        self, query: ContractorFilterDTO
    ) -> List[Contractor]:
        pass
