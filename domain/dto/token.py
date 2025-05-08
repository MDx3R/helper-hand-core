from datetime import datetime
from typing import Literal
from domain.dto.base import ApplicationDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO


class TokenClaims(ApplicationDTO):
    user: UserContextDTO
    type: Literal["access", "refresh"]
    exp: datetime

    @property
    def is_access(self) -> bool:
        return self.type == "access"

    @property
    def is_refresh(self) -> bool:
        return self.type == "refresh"
