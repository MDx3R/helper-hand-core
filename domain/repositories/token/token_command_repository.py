from abc import ABC, abstractmethod

from domain.entities.token.token import Token


class TokenCommandRepository(ABC):
    @abstractmethod
    async def create_token(self, token: Token) -> Token:
        pass

    @abstractmethod
    async def revoke_token(self, token: str) -> Token:
        pass
