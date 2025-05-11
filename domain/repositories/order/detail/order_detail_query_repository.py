from abc import ABC, abstractmethod
from typing import List

from domain.entities.order.detail import OrderDetail


class OrderDetailQueryRepository(ABC):
    @abstractmethod
    async def get_detail(self, detail_id: int) -> OrderDetail | None:
        pass

    @abstractmethod
    async def get_details_by_order_id(
        self, order_id: int
    ) -> List[OrderDetail]:
        pass

    @abstractmethod
    async def get_available_order_details(
        self, order_id: int
    ) -> List[OrderDetail]:
        pass
