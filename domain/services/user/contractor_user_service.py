from abc import ABC, abstractmethod

from domain.models import User, Contractor

class ContractorUserService(ABC):
    @abstractmethod
    async def get_user(self, user_id: int, contractor: Contractor) -> User | None:
        pass

    @abstractmethod
    async def get_profile(self, contractor: Contractor) -> Contractor:
        pass