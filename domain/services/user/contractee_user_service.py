from abc import ABC, abstractmethod

from domain.models import Contractee

class ContracteeUserService(ABC):
    @abstractmethod
    async def get_profile(self, contractee: Contractee) -> Contractee:
        pass