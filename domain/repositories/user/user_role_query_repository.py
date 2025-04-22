from abc import ABC, abstractmethod
from typing import TypeVar

from domain.dto.user.internal.base import UserIdDTO
from domain.entities.user.admin import Admin
from domain.entities.user.contractee import Contractee
from domain.entities.user.contractor import Contractor

Role = TypeVar("Role", Admin, Contractee, Contractor)


class UserRoleQueryRepository(ABC):
    @abstractmethod
    async def get_user(self, query: UserIdDTO) -> Role | None:
        pass

    @abstractmethod
    async def get_first_pending_user(
        self,
    ) -> Contractee | Contractor | None:
        pass
