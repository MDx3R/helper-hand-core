from abc import ABC, abstractmethod

from domain.entities.user.admin.admin import Admin


class AdminOrderQueryRepository(ABC):
    # TODO: Переместить в AdminQueryRepository
    @abstractmethod
    async def get_admin(self, order_id: int) -> Admin | None:
        pass
