from abc import ABC, abstractmethod

from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
)


class ContracteeUserQueryService(ABC):
    @abstractmethod
    async def get_profile(
        self, context: UserContextDTO
    ) -> ContracteeOutputDTO:
        pass
