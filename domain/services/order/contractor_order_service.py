from abc import ABC, abstractmethod
from typing import List

from domain.dto.order.internal.order_managment_dto import (
    CancelOrderDTO,
    SetOrderActiveDTO,
)
from domain.dto.order.internal.order_query_dto import GetOrderDTO
from domain.dto.order.request.create_order_dto import CreateOrderDTO
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO


class ContractorOrderManagementService(ABC):
    @abstractmethod
    async def create_order(
        self, request: CreateOrderDTO
    ) -> OrderWithDetailsOutputDTO:
        pass

    @abstractmethod
    async def cancel_order(self, request: CancelOrderDTO) -> OrderOutputDTO:
        pass

    @abstractmethod
    async def set_order_active(
        self, request: SetOrderActiveDTO
    ) -> OrderOutputDTO:
        pass


class ContractorOrderQueryService(ABC):
    @abstractmethod
    async def get_order(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        pass

    @abstractmethod
    async def get_orders(
        self, context: UserContextDTO
    ) -> List[OrderOutputDTO]:
        pass
