from abc import ABC, abstractmethod
from typing import List

from domain.dto.order.internal.order_filter_dto import DetailFilterDTO
from domain.entities.user.contractee import Contractee


class ContracteeOrderQueryRepository(ABC):
    @abstractmethod
    async def get_contractees(
        self, query: DetailFilterDTO
    ) -> List[Contractee]:
        pass
