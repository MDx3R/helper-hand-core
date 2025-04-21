from abc import ABC, abstractmethod
from typing import List

from domain.dto.order.internal.base import DetailIdDTO, OrderIdDTO
from domain.entities.order.detail import OrderDetail


class OrderDetailQueryRepository(ABC):
    @abstractmethod
    async def get_detail(self, query: DetailIdDTO) -> OrderDetail | None:
        pass

    @abstractmethod
    async def get_details_by_order_id(
        self, query: OrderIdDTO
    ) -> List[OrderDetail]:
        pass

    @abstractmethod
    async def get_available_order_details(
        self, query: OrderIdDTO
    ) -> List[OrderDetail]:
        pass


class OrderDetailCommandRepository(ABC):
    @abstractmethod
    async def update_detail(self, detail: OrderDetail) -> OrderDetail:
        pass

    @abstractmethod
    async def create_detail(self, detail: OrderDetail) -> OrderDetail:
        pass

    @abstractmethod
    async def create_details(
        self, details: List[OrderDetail]
    ) -> List[OrderDetail]:
        pass
