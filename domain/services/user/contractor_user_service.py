from abc import ABC, abstractmethod

from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO
from domain.dto.context import UserContextDTO
from domain.dto.internal import GetUserWithContextDTO

class ContractorUserQueryService(ABC):
    @abstractmethod
    async def get_user(self, query: GetUserWithContextDTO) -> ContractorDTO | ContracteeDTO | None:
        pass

    @abstractmethod
    async def get_profile(self, context: UserContextDTO) -> ContractorDTO:
        pass