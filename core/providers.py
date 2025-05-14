from core.config import AuthConfig, DatabaseConfig


def load_auth_config(path: str = "config/auth.yaml") -> AuthConfig:
    return AuthConfig()


def load_database_config(path: str = "config/db.yaml") -> DatabaseConfig:
    return DatabaseConfig(
        DB_NAME="HelperHand",
        DB_USER="postgres",
        DB_PASSWORD="246224682",
        DB_HOST="127.0.0.1",
        DB_PORT="5432",
    )
