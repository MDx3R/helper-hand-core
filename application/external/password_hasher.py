from abc import ABC, abstractmethod

import bcrypt


class PasswordHasher(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        """Хэширует пароль и возвращает строку хэша."""
        pass

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool:
        """Проверяет, соответствует ли пароль хэшу."""
        pass


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
