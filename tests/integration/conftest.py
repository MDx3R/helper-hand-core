import pytest

from core.config import Config
from infrastructure.database.database import Database


@pytest.fixture(scope="session")
def config():
    return Config.load_from_path("config/test_config.yaml")


@pytest.fixture(scope="session")
def database(config: Config):
    return Database(config.db)
