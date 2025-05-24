from typing import List
from abc import ABC, abstractmethod

from domain.dto.base import LastObjectDTO, PaginationDTO
from domain.dto.order.response.order_output_dto import (
    OrderOutputDTO,
)


class OrderQueryService(ABC):
    @abstractmethod
    async def get_recent_orders(
        self, query: PaginationDTO
    ) -> List[OrderOutputDTO]:
        pass
