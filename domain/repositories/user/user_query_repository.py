from abc import ABC, abstractmethod
from typing import List

from domain.dto.user.internal.user_filter_dto import UserFilterDTO
from domain.entities.user.context import UserContext
from domain.entities.user.credentials import (
    WebCredentials,
)
from domain.entities.user.user import User


class UserQueryRepository(ABC):
    @abstractmethod
    async def get_user(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def filter_users(self, query: UserFilterDTO) -> List[User]:
        pass

    @abstractmethod
    async def exists_by_query(self, query: UserFilterDTO) -> bool:
        pass

    @abstractmethod
    async def get_web_credentials_by_email(
        self, email: str
    ) -> WebCredentials | None:
        pass

    @abstractmethod
    async def get_user_context_by_email(
        self, email: str
    ) -> UserContext | None:
        pass
