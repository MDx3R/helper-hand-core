from dataclasses import dataclass
from datetime import timedelta


@dataclass
class AuthConfig:
    SECRET_KEY: str = "secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRATION_TIME: timedelta = timedelta(days=7, minutes=30)
    REFRESH_TOKEN_EXPIRATION_TIME: timedelta = timedelta(days=7)
