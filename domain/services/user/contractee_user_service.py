from abc import ABC, abstractmethod

from domain.models import Contractee
from application.dtos.output import ContracteeOutputDTO

class ContracteeUserService(ABC):
    @abstractmethod
    async def get_profile(self, contractee: Contractee) -> ContracteeOutputDTO:
        pass