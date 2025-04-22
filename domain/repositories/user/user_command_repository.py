from abc import ABC, abstractmethod

from domain.dto.user.internal.user_command_dto import SetUserStatusDTO
from domain.entities.user.telegram_user import TelegramUser
from domain.entities.user.user import User


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
