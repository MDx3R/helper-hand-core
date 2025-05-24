from abc import ABC, abstractmethod
from typing import List

from domain.dto.user.internal.user_filter_dto import UserFilterDTO
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
        self, user_id: int
    ) -> Admin | Contractee | Contractor | None:
        pass

    @abstractmethod
    async def get_complete_user(
        self, user_id: int
    ) -> CompleteAdmin | CompleteContractee | CompleteContractor | None:
        pass

    @abstractmethod
    async def filter_users(
        self, query: UserFilterDTO
    ) -> List[CompleteContractee | CompleteContractor]:
        pass
