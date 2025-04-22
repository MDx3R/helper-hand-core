from abc import ABC, abstractmethod

from domain.dto.order.internal.base import OrderIdDTO
from domain.entities.user.admin import Admin


class AdminOrderQueryRepository(ABC):
    @abstractmethod
    async def get_admin(self, query: OrderIdDTO) -> Admin | None:
        pass
