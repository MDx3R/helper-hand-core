from abc import ABC, abstractmethod

from domain.entities.user.admin import Admin


class AdminCommandRepository(ABC):
    @abstractmethod
    async def create_admin(self, admin: Admin) -> Admin:
        pass

    @abstractmethod
    async def update_admin(self, admin: Admin) -> Admin:
        pass
