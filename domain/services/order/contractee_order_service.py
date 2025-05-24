from typing import List
from abc import ABC, abstractmethod

from domain.dto.order.internal.order_query_dto import (
    GetOrderAfterDTO,
    GetOrderDTO,
)
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderDetailOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)
from domain.dto.user.internal.user_context_dto import PaginatedDTO


class ContracteeOrderQueryService(ABC):
    @abstractmethod
    async def get_order(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        pass

    @abstractmethod
    async def get_suitable_orders(
        self, query: PaginatedDTO
    ) -> List[OrderWithDetailsOutputDTO]:
        pass

    @abstractmethod
    async def get_suitable_details_for_order(
        self, query: GetOrderDTO
    ) -> List[OrderDetailOutputDTO]:
        pass

    @abstractmethod
    async def get_orders(self, query: PaginatedDTO) -> List[OrderOutputDTO]:
        pass
