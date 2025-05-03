from abc import ABC, abstractmethod
from typing import List

from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.dto.order.internal.order_query_dto import GetUserOrdersDTO
from domain.dto.order.response.order_output_dto import OrderOutputDTO


class OrderQueryService(ABC):
    @abstractmethod
    async def filter_orders(
        self, query: OrderFilterDTO
    ) -> List[OrderOutputDTO]:
        pass


class UserAssociatedOrderQueryService(ABC):
    @abstractmethod
    async def get_contractee_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderOutputDTO]:
        pass

    @abstractmethod
    async def get_contractor_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderOutputDTO]:
        pass

    @abstractmethod
    async def get_admin_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderOutputDTO]:
        pass
