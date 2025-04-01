from abc import ABC, abstractmethod

from domain.dto.common import ContracteeDTO
from domain.dto.context import UserContextDTO

class ContracteeUserQueryService(ABC):
    @abstractmethod
    async def get_profile(self, context: UserContextDTO) -> ContracteeDTO:
        pass