from abc import ABC, abstractmethod
from typing import List

from domain.dto.order.internal.base import OrderIdDTO
from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.entities.order.order_with_details import (
    CompleteOrder,
    OrderWithDetails,
    OrderWithDetailsAndContractor,
    OrderWithDetailsAndSupervisor,
)


class CompositeOrderQueryRepository(ABC):
    @abstractmethod
    async def get_order_with_details(
        self, query: OrderIdDTO
    ) -> OrderWithDetails | None:
        pass

    @abstractmethod
    async def get_order_with_details_and_contractor(
        self, query: OrderIdDTO
    ) -> OrderWithDetailsAndContractor | None:
        pass

    @abstractmethod
    async def get_order_with_details_and_supervisor(
        self, query: OrderIdDTO
    ) -> OrderWithDetailsAndSupervisor | None:
        pass

    @abstractmethod
    async def get_complete_order(
        self, query: OrderIdDTO
    ) -> CompleteOrder | None:
        pass

    @abstractmethod
    async def filter_orders_with_details(
        self, query: OrderFilterDTO
    ) -> List[OrderWithDetails]:
        pass

    @abstractmethod
    async def filter_orders_with_details_and_contractor(
        self, query: OrderFilterDTO
    ) -> List[OrderWithDetailsAndContractor]:
        pass

    @abstractmethod
    async def filter_orders_with_details_and_supervisor(
        self, query: OrderFilterDTO
    ) -> List[OrderWithDetailsAndSupervisor]:
        pass

    @abstractmethod
    async def filter_complete_orders(
        self, query: OrderFilterDTO
    ) -> List[CompleteOrder]:
        pass
