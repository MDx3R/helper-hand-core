from abc import ABC, abstractmethod

from domain.dto.order.internal.user_command_dto import (
    SetOrderAdminDTO,
    SetOrderStatusDTO,
)
from domain.entities.order.order import Order


class OrderCommandRepository(ABC):
    @abstractmethod
    async def create_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def update_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def set_order_status(self, query: SetOrderStatusDTO) -> Order:
        pass

    @abstractmethod
    async def set_order_admin(self, query: SetOrderAdminDTO) -> Order:
        pass
