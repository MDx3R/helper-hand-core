from core.config import AuthConfig


def load_auth_config(path: str = "config/auth.yaml") -> AuthConfig:
    return AuthConfig()
