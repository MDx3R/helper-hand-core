from abc import ABC, abstractmethod

from domain.entities.user.contractee import Contractee


class ContracteeCommandRepository(ABC):
    @abstractmethod
    async def create_contractee(self, contractee: Contractee) -> Contractee:
        pass

    @abstractmethod
    async def update_contractor(self, contractee: Contractee) -> Contractee:
        pass
