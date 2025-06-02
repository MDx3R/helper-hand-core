from abc import ABC, abstractmethod

from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.internal.user_query_dto import GetUserDTO
from domain.dto.user.request.contractee.contractee_registration_dto import (
    UpdateContracteeDTO,
)
from domain.dto.user.response.admin.admin_output_dto import (
    CompleteAdminOutputDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
    ContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)


class ContracteeUserQueryService(ABC):
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
    ) -> CompleteContracteeOutputDTO:
        pass

    @abstractmethod
    async def update_profile(
        self, query: UpdateContracteeDTO
    ) -> ContracteeOutputDTO:
        pass
