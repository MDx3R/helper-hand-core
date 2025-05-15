from datetime import datetime
from typing import Optional
from domain.entities.base import ApplicationModel
from domain.entities.token.enums import TokenTypeEnum


class Token(ApplicationModel):
    token_id: Optional[int] = None
    """Уникальный идентификатор токена. Может быть `None` только при создании нового токена."""

    user_id: int
    token: str
    type: TokenTypeEnum
    revoked: bool = False
    expires_at: datetime
