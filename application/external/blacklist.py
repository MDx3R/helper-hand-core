from abc import ABC, abstractmethod


class TokenBlacklist(ABC):
    @abstractmethod
    async def add(self, token: str, expires_at: float):
        pass

    @abstractmethod
    async def contains(self, token: str) -> bool:
        pass
