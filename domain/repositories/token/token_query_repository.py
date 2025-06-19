from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from domain.dto.token import TokenFilter, TokenSignature
from domain.entities.token.token import Token, TokenPair


class TokenQueryRepository(ABC):
    @abstractmethod
    async def get_token(self, signature: TokenSignature) -> Token | None:
        pass

    @abstractmethod
    async def get_tokens(self, query: TokenFilter) -> List[Token]:
        pass

    @abstractmethod
    async def get_token_pair_by_session(
        self, session_id: UUID
    ) -> TokenPair | None:
        pass
