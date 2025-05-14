from argparse import ArgumentParser
from datetime import timedelta
import os
from pathlib import Path

from pydantic import BaseModel
import yaml


class AuthConfig(BaseModel):
    SECRET_KEY: str = "secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRATION_TIME: timedelta = timedelta(days=7, minutes=30)
    REFRESH_TOKEN_EXPIRATION_TIME: timedelta = timedelta(days=7)


class DatabaseConfig(BaseModel):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DBMS: str = "postgresql"

    @property
    def database_url(self):
        return (
            f"{self.DBMS}+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class Config(BaseModel):
    auth: AuthConfig
    db: DatabaseConfig

    @classmethod
    def load(cls) -> "Config":
        path = cls.fetch_config_path()
        return cls.load_from_path(path)

    @staticmethod
    def load_from_path(path: str | Path) -> "Config":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found at: {path}")

        with path.open("r") as f:
            data = yaml.safe_load(f)

        return Config.model_validate(data)

    @staticmethod
    def fetch_config_path() -> Path:
        default = "config/config.yaml"

        parser = ArgumentParser(description="Load config path")
        parser.add_argument("--config", type=str, help="Path to config file")
        args, _ = parser.parse_known_args()

        return Path(args.config or os.getenv("CONFIG_PATH") or default)
