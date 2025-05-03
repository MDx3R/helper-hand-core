from abc import ABC, abstractmethod


class UserTokenService(ABC):
    @abstractmethod
    async def generate_token(self):
        pass

    @abstractmethod
    async def refresh_token(self):
        pass


class UserVerificationService(ABC):
    """
    Интерфейс для сервисов аутентификации и авторизации пользователей.
    """

    @abstractmethod
    async def verify_telegram(self):
        pass

    @abstractmethod
    async def verify_web(self):
        pass
