from abc import ABC, abstractmethod

from domain.entities import User, Admin

from domain.dto.common import UserDTO

class AdminUserService(ABC):
    @abstractmethod
    async def get_user(self, user_id: int, admin: Admin) -> UserDTO | None:
        pass

    @abstractmethod
    async def get_first_pending_user(self, admin: Admin) -> UserDTO | None:
        pass

    @abstractmethod
    async def approve_registration(self, user_id: int, admin: Admin) -> UserDTO:
        pass

    @abstractmethod
    async def disapprove_registration(self, user_id: int, admin: Admin) -> UserDTO:
        pass

    @abstractmethod
    async def drop_user(self, user_id: int, admin: Admin) -> UserDTO:
        pass

    @abstractmethod
    async def ban_user(self, user_id: int, admin: Admin) -> UserDTO:
        pass

    @abstractmethod
    async def notify_user(self, user_id: int, admin: Admin):
        pass