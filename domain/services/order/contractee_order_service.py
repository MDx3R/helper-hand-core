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
)
from domain.dto.user.internal.user_context_dto import UserContextDTO


class ContracteeOrderQueryService(ABC):
    @abstractmethod
    async def get_order(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        pass

    @abstractmethod
    async def get_suitable_order(
        self, query: GetOrderAfterDTO
    ) -> CompleteOrderOutputDTO | None:
        pass

    @abstractmethod
    async def get_suitable_details(
        self, query: GetOrderDTO
    ) -> List[OrderDetailOutputDTO]:
        pass

    @abstractmethod
    async def get_orders(
        self, context: UserContextDTO
    ) -> List[OrderOutputDTO]:
        pass
