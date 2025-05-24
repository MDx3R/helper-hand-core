from abc import ABC, abstractmethod
from typing import List

from domain.dto.base import LastObjectDTO
from domain.dto.order.internal.order_managment_dto import (
    ApproveOrderDTO,
    CancelOrderDTO,
    CloseOrderDTO,
    DisapproveOrderDTO,
    FulfillOrderDTO,
    OpenOrderDTO,
    SetOrderActiveDTO,
    TakeOrderDTO,
)
from domain.dto.order.internal.order_query_dto import (
    GetOrderDTO,
    GetUserOrdersDTO,
)
from domain.dto.order.request.create_order_dto import CreateOrderDTO
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)
from domain.dto.user.internal.user_context_dto import PaginatedDTO


class AdminOrderManagementService(ABC):
    @abstractmethod
    async def create_order(
        self, request: CreateOrderDTO
    ) -> OrderWithDetailsOutputDTO:
        pass

    @abstractmethod
    async def take_order(self, request: TakeOrderDTO) -> OrderOutputDTO:
        pass

    @abstractmethod
    async def approve_order(self, request: ApproveOrderDTO) -> OrderOutputDTO:
        pass

    @abstractmethod
    async def disapprove_order(
        self, request: DisapproveOrderDTO
    ) -> OrderOutputDTO:
        pass

    @abstractmethod
    async def cancel_order(self, request: CancelOrderDTO) -> OrderOutputDTO:
        pass

    @abstractmethod
    async def close_order(self, request: CloseOrderDTO) -> OrderOutputDTO:
        pass

    @abstractmethod
    async def open_order(self, request: OpenOrderDTO) -> OrderOutputDTO:
        pass

    @abstractmethod
    async def set_order_active(
        self, request: SetOrderActiveDTO
    ) -> OrderOutputDTO:
        pass

    @abstractmethod
    async def fulfill_order(self, request: FulfillOrderDTO) -> OrderOutputDTO:
        pass


class AdminOrderQueryService(ABC):
    @abstractmethod
    async def get_order(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        pass

    @abstractmethod
    async def get_unassigned_orders(
        self, query: PaginatedDTO
    ) -> List[OrderOutputDTO]:
        pass

    @abstractmethod
    async def get_orders(self, query: PaginatedDTO) -> List[OrderOutputDTO]:
        pass

    @abstractmethod
    async def get_user_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderOutputDTO]:
        pass
