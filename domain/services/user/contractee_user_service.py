from abc import ABC, abstractmethod

from domain.entities import Contractee
from domain.dto.common import ContracteeDTO

class ContracteeUserService(ABC):
    @abstractmethod
    async def get_profile(self, contractee: Contractee) -> ContracteeDTO:
        pass