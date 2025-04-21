from abc import ABC, abstractmethod
from typing import TypeVar, List
from domain.dto.user.internal.base import (
    UserIdDTO,
    UserWithCredentialsDTO,
)
from domain.dto.user.internal.user_command_dto import SetUserStatusDTO
from domain.dto.user.internal.user_filter_dto import (
    AdminFilterDTO,
    ContracteeFilterDTO,
    ContractorFilterDTO,
    UserFilterDTO,
)
from domain.entities.user.admin import Admin
from domain.entities.user.contractee import Contractee
from domain.entities.user.contractor import Contractor
from domain.entities.user.telegram_user import TelegramUser
from domain.entities.user.user import User

Role = TypeVar("Role", Admin, Contractee, Contractor)


class UserQueryRepository(ABC):
    @abstractmethod
    async def get_user(self, query: UserIdDTO) -> User | None:
        pass

    @abstractmethod
    async def filter_users(self, query: UserFilterDTO) -> List[User]:
        pass

    @abstractmethod
    async def get_user_with_credentials(
        self, query: UserWithCredentialsDTO
    ) -> User | None:
        pass

    @abstractmethod
    async def exists_by_query(self, query: UserFilterDTO) -> bool:
        pass


class AdminQueryRepository(ABC):
    @abstractmethod
    async def get_admin(self, query: UserIdDTO) -> Admin | None:
        pass

    @abstractmethod
    async def filter_admins(self, query: AdminFilterDTO) -> List[Admin]:
        pass


class ContractorQueryRepository(ABC):
    @abstractmethod
    async def get_contractor(self, query: UserIdDTO) -> Contractor | None:
        pass

    @abstractmethod
    async def filter_contractors(
        self, query: ContractorFilterDTO
    ) -> List[Contractor]:
        pass


class ContracteeQueryRepository(ABC):
    @abstractmethod
    async def get_contractee(self, query: UserIdDTO) -> Contractee | None:
        pass

    @abstractmethod
    async def filter_contractees(
        self, query: ContracteeFilterDTO
    ) -> List[Contractee]:
        pass


class UserRoleQueryRepository(ABC):
    @abstractmethod
    async def get_user(self, query: UserIdDTO) -> Role | None:
        pass

    @abstractmethod
    async def get_first_pending_user(
        self,
    ) -> Contractee | Contractor | None:
        pass


class UserCommandRepository(ABC):
    @abstractmethod
    async def set_user_status(self, query: SetUserStatusDTO) -> None:
        pass

    @abstractmethod
    async def create_telegram_user(self, user: TelegramUser) -> TelegramUser:
        pass

    @abstractmethod
    async def update_user(self, user: User) -> User:
        pass


class AdminCommandRepository(ABC):
    @abstractmethod
    async def create_admin(self, admin: Admin) -> Admin:
        pass

    @abstractmethod
    async def update_admin(self, admin: Admin) -> Admin:
        pass


class ContractorCommandRepository(ABC):
    @abstractmethod
    async def create_contractor(self, contractor: Contractor) -> Contractor:
        pass

    @abstractmethod
    async def update_contractor(self, contractor: Contractor) -> Contractor:
        pass


class ContracteeCommandRepository(ABC):
    @abstractmethod
    async def create_contractee(self, contractee: Contractee) -> Contractee:
        pass

    @abstractmethod
    async def update_contractor(self, contractee: Contractee) -> Contractee:
        pass


class UserRoleCommandRepository(ABC):
    @abstractmethod
    async def create_user(self, role: Role) -> Role:
        pass

    @abstractmethod
    async def update_user(self, role: Role) -> Role:
        pass
