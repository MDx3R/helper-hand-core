from abc import ABC, abstractmethod

from domain.dto.token import TokenClaims
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.response.user_output_dto import AuthOutputDTO


class TokenService(ABC):
    @abstractmethod
    async def generate_token(self, context: UserContextDTO) -> AuthOutputDTO:
        pass

    @abstractmethod
    async def refresh_token(self, token: str) -> AuthOutputDTO:
        pass

    @abstractmethod
    async def get_user_context(self, token: str) -> UserContextDTO:
        pass

    @abstractmethod
    async def extract_claims(self, token: str) -> TokenClaims:
        pass
