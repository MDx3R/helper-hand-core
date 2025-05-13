from abc import ABC, abstractmethod

from domain.dto.user.internal.user_command_dto import SetUserStatusDTO
from domain.entities.user.credentials import (
    TelegramCredentials,
    WebCredentials,
)
from domain.entities.user.user import User


class UserCommandRepository(ABC):
    @abstractmethod
    async def set_user_status(self, query: SetUserStatusDTO) -> User:
        pass

    @abstractmethod
    async def create_telegram_user(
        self, user: TelegramCredentials
    ) -> TelegramCredentials:
        pass

    @abstractmethod
    async def create_web_user(self, user: WebCredentials) -> WebCredentials:
        pass

    @abstractmethod
    async def update_user(self, user: User) -> User:
        pass
