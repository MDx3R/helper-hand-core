from abc import ABC, abstractmethod
from typing import TypeVar

from domain.dto.user.internal.base import UserIdDTO
from domain.entities.user.admin.admin import Admin
from domain.entities.user.admin.composite_admin import CompleteAdmin
from domain.entities.user.contractee.composite_contractee import (
    CompleteContractee,
)
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.composite_contractor import (
    CompleteContractor,
)
from domain.entities.user.contractor.contractor import Contractor


class UserRoleQueryRepository(ABC):
    @abstractmethod
    async def get_user(
        self, query: UserIdDTO
    ) -> Admin | Contractee | Contractor | None:
        pass

    @abstractmethod
    async def get_complete_user(
        self, query: UserIdDTO
    ) -> CompleteAdmin | CompleteContractee | CompleteContractor | None:
        pass

    @abstractmethod
    async def get_first_pending_user(
        self,
    ) -> CompleteContractee | CompleteContractor | None:
        pass
