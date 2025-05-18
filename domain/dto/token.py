from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import UUID4
from domain.dto.base import ApplicationDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.entities.token.enums import TokenTypeEnum


class TokenClaims(ApplicationDTO):
    user: UserContextDTO
    session: UUID4
    type: TokenTypeEnum
    exp: datetime
    """Дата и вермя истечения токена"""

    @property
    def is_access(self) -> bool:
        return self.type == TokenTypeEnum.access

    @property
    def is_refresh(self) -> bool:
        return self.type == TokenTypeEnum.refresh


class TokenFilter(ApplicationDTO):
    user_id: Optional[int] = None
    session_id: Optional[UUID] = None
    type: Optional[TokenTypeEnum] = None
    revoked: Optional[bool] = None
    expired: Optional[bool] = None


class TokenSignature(TokenFilter):
    token: str
