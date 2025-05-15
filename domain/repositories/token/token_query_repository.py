from abc import ABC, abstractmethod
from typing import List

from domain.dto.token import TokenFilter, TokenSignature
from domain.entities.token.token import Token


class TokenQueryRepository(ABC):
    @abstractmethod
    async def get_token(self, signature: TokenSignature) -> Token | None:
        pass

    @abstractmethod
    async def get_tokens(self, query: TokenFilter) -> List[Token]:
        pass
