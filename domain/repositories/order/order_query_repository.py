from abc import ABC, abstractmethod
from typing import List

from domain.dto.order.internal.base import (
    DetailIdDTO,
    OrderIdDTO,
    OrderSignatureDTO,
)
from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.entities.order.order import Order


class OrderQueryRepository(ABC):
    @abstractmethod
    async def get_order(self, query: OrderIdDTO) -> Order | None:
        pass

    @abstractmethod
    async def get_order_for_detail(self, query: DetailIdDTO) -> Order | None:
        pass

    @abstractmethod
    async def get_order_by_signature(
        self, query: OrderSignatureDTO
    ) -> Order | None:
        pass

    @abstractmethod
    async def filter_orders(self, query: OrderFilterDTO) -> List[Order]:
        pass
