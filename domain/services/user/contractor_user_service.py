from abc import ABC, abstractmethod

from domain.entities import User, Contractor
from application.dtos.output import UserOutputDTO

class ContractorUserService(ABC):
    @abstractmethod
    async def get_user(self, user_id: int, contractor: Contractor) -> UserOutputDTO | None:
        pass

    @abstractmethod
    async def get_profile(self, contractor: Contractor) -> Contractor:
        pass