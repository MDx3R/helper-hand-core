from abc import ABC, abstractmethod


class TokenBlacklist(ABC):
    @abstractmethod
    def add(self, token: str, expires_at: float):
        pass

    @abstractmethod
    def contains(self, token: str) -> bool:
        pass
