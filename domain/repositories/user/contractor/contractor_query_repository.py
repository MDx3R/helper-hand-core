from abc import ABC, abstractmethod
from typing import List

from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_filter_dto import (
    ContractorFilterDTO,
)
from domain.entities.user.contractor import Contractor


class ContractorQueryRepository(ABC):
    @abstractmethod
    async def get_contractor(self, query: UserIdDTO) -> Contractor | None:
        pass

    @abstractmethod
    async def filter_contractors(
        self, query: ContractorFilterDTO
    ) -> List[Contractor]:
        pass
