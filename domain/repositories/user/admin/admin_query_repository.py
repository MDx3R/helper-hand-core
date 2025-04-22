from abc import ABC, abstractmethod
from typing import List

from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_filter_dto import (
    AdminFilterDTO,
)
from domain.entities.user.admin import Admin


class AdminQueryRepository(ABC):
    @abstractmethod
    async def get_admin(self, query: UserIdDTO) -> Admin | None:
        pass

    @abstractmethod
    async def filter_admins(self, query: AdminFilterDTO) -> List[Admin]:
        pass
