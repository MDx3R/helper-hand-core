from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from domain.entities.token.token import Token


class TokenCommandRepository(ABC):
    @abstractmethod
    async def create_token(self, token: Token) -> Token:
        pass

    @abstractmethod
    async def revoke_token(self, token: str) -> Token:
        pass

    @abstractmethod
    async def revoke_tokens_by_session(self, session: UUID) -> List[Token]:
        pass
