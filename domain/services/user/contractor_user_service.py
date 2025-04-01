from abc import ABC, abstractmethod

from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO
from domain.dto.context import UserContextDTO

class ContractorUserQueryService(ABC):
    @abstractmethod
    async def get_user(self, user_id: int, context: UserContextDTO) -> ContractorDTO | ContracteeDTO | None:
        pass

    @abstractmethod
    async def get_profile(self, context: UserContextDTO) -> ContractorDTO:
        pass