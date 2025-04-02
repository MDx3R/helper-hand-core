from abc import ABC, abstractmethod

from domain.dto.common import UserDTO, AdminDTO, ContracteeDTO, ContractorDTO
from domain.dto.internal import (
    GetUserDTO, 
    UserManagementDTO, 
    UserNotificationDTO
)

class AdminUserQueryService(ABC):
    @abstractmethod
    async def get_user(self, query: GetUserDTO) -> AdminDTO | ContracteeDTO | ContractorDTO | None:
        pass

    @abstractmethod
    async def get_pending_user(self) -> ContracteeDTO | ContractorDTO | None:
        pass

class AdminUserManagementService(ABC):
    @abstractmethod
    async def drop_user(self, query: UserManagementDTO) -> UserDTO:
        pass

    @abstractmethod
    async def ban_user(self, query: UserManagementDTO) -> UserDTO:
        pass

class AdminUserApprovalService(ABC):
    @abstractmethod
    async def approve_registration(self, query: UserManagementDTO) -> UserDTO:
        pass

    @abstractmethod
    async def disapprove_registration(self, query: UserManagementDTO) -> UserDTO:
        pass

class AdminUserNotificationService(ABC):
    @abstractmethod
    async def notify_user(self, notification: UserNotificationDTO):
        pass