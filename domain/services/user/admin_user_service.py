from abc import ABC, abstractmethod

from domain.dto.common import UserDTO
from domain.dto.context import UserContextDTO

class AdminUserQueryService(ABC):
    @abstractmethod
    async def get_user(self, user_id: int) -> UserDTO | None:
        pass

    @abstractmethod
    async def get_first_pending_user(self) -> UserDTO | None:
        pass

class AdminUserManagementService(ABC):
    @abstractmethod
    async def drop_user(self, user_id: int, context: UserContextDTO) -> UserDTO:
        pass

    @abstractmethod
    async def ban_user(self, user_id: int, context: UserContextDTO) -> UserDTO:
        pass

class AdminUserApprovalService(ABC):
    @abstractmethod
    async def approve_registration(self, user_id: int, context: UserContextDTO) -> UserDTO:
        pass

    @abstractmethod
    async def disapprove_registration(self, user_id: int, context: UserContextDTO) -> UserDTO:
        pass

class AdminUserNotificationService(ABC):
    @abstractmethod
    async def notify_user(self, user_id: int, context: UserContextDTO):
        pass