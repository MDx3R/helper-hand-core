from abc import ABC, abstractmethod
from typing import List

from domain.entities.order.detail import OrderDetail


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
