from abc import ABC, abstractmethod

from domain.entities import Contractee
from domain.dto.output import ContracteeOutputDTO

class ContracteeUserService(ABC):
    @abstractmethod
    async def get_profile(self, contractee: Contractee) -> ContracteeOutputDTO:
        pass