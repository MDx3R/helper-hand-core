from abc import ABC, abstractmethod
from typing import List

from domain.dto.user.internal.user_context_dto import (
    PaginatedDTO,
    UserContextDTO,
)
from domain.dto.user.internal.user_managment_dto import (
    ApproveUserDTO,
    BanUserDTO,
    DisapproveUserDTO,
    DropUserDTO,
)

from domain.dto.user.internal.user_query_dto import GetUserDTO
from domain.dto.user.request.admin.create_admin_dto import UpdateAdminDTO
from domain.dto.user.response.admin.admin_output_dto import (
    AdminOutputDTO,
    CompleteAdminOutputDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)
from domain.dto.user.response.user_output_dto import UserOutputDTO


class AdminUserQueryService(ABC):
    @abstractmethod
    async def get_user(
        self, query: GetUserDTO
    ) -> (
        CompleteAdminOutputDTO
        | CompleteContracteeOutputDTO
        | CompleteContractorOutputDTO
        | None
    ):
        pass

    @abstractmethod
    async def get_profile(
        self, context: UserContextDTO
    ) -> CompleteAdminOutputDTO:
        pass

    @abstractmethod
    async def get_pending_users(
        self, query: PaginatedDTO
    ) -> List[UserOutputDTO]:
        pass

    @abstractmethod
    async def update_profile(self, query: UpdateAdminDTO) -> AdminOutputDTO:
        pass


class AdminUserManagementService(ABC):
    @abstractmethod
    async def approve_user(self, request: ApproveUserDTO) -> UserOutputDTO:
        pass

    @abstractmethod
    async def disapprove_user(
        self, request: DisapproveUserDTO
    ) -> UserOutputDTO:
        pass

    @abstractmethod
    async def drop_user(self, request: DropUserDTO) -> UserOutputDTO:
        pass

    @abstractmethod
    async def ban_user(self, request: BanUserDTO) -> UserOutputDTO:
        pass
