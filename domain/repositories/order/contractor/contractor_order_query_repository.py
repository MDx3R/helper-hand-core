from abc import ABC, abstractmethod

from domain.dto.order.internal.base import OrderIdDTO
from domain.entities.user.contractor import Contractor


class ContractorOrderQueryRepository(ABC):
    @abstractmethod
    async def get_contractor(self, query: OrderIdDTO) -> Contractor | None:
        pass
