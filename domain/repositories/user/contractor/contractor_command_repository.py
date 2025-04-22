from abc import ABC, abstractmethod

from domain.entities.user.contractor import Contractor


class ContractorCommandRepository(ABC):
    @abstractmethod
    async def create_contractor(self, contractor: Contractor) -> Contractor:
        pass

    @abstractmethod
    async def update_contractor(self, contractor: Contractor) -> Contractor:
        pass
