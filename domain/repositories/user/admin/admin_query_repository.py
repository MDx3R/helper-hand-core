from abc import ABC, abstractmethod
from typing import List

from domain.dto.user.internal.user_filter_dto import (
    AdminFilterDTO,
)
from domain.entities.user.admin.admin import Admin
from domain.entities.user.admin.composite_admin import (
    AdminWithContractor,
    CompleteAdmin,
)


class AdminQueryRepository(ABC):
    @abstractmethod
    async def get_admin(self, user_id: int) -> Admin | None:
        pass

    @abstractmethod
    async def get_admin_and_contractor(
        self, user_id: int
    ) -> AdminWithContractor | None:
        pass

    @abstractmethod
    async def get_complete_admin(self, user_id: int) -> CompleteAdmin | None:
        pass

    @abstractmethod
    async def filter_admins(self, query: AdminFilterDTO) -> List[Admin]:
        pass
