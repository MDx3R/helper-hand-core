from abc import ABC, abstractmethod
from typing import List

from domain.dto.user.internal.user_filter_dto import UserFilterDTO
from domain.dto.user.internal.user_query_dto import GetUserDTO
from domain.dto.user.response.admin.admin_output_dto import AdminOutputDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
)
from domain.dto.user.response.user_output_dto import UserOutputDTO


class UserQueryService(ABC):
    @abstractmethod
    async def get_user(
        self, query: GetUserDTO
    ) -> AdminOutputDTO | ContracteeOutputDTO | ContractorOutputDTO | None:
        pass

    @abstractmethod
    async def filter_users(self, query: UserFilterDTO) -> List[UserOutputDTO]:
        pass
