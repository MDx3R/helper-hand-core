from datetime import datetime
from uuid import uuid4

from domain.entities.token.enums import TokenTypeEnum
from domain.entities.token.token import Token
from infrastructure.database.models import TokenBase


def get_base() -> TokenBase:
    """Создать базовую модель TokenBase для тестов."""
    return TokenBase(
        token="testtoken",
        user_id=1,
        type=TokenTypeEnum.access,
        revoked=False,
        expires_at=datetime.now(),
        session_id=uuid4(),
    )


def get_token() -> Token:
    """Создать сущность Token для тестов."""
    return Token(
        token="testtoken",
        user_id=1,
        type=TokenTypeEnum.access,
        revoked=False,
        expires_at=datetime.now(),
        session_id=uuid4(),
    )
