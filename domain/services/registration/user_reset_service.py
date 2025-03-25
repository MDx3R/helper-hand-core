from abc import ABC, abstractmethod

from domain.dto.input.registration import UserResetDTO
from domain.dto.common import UserDTO
from domain.dto.context import UserContextDTO

class UserResetService(ABC):
    """
    Интерфейс для сервисов повторной регистрации пользователей.
    """
    @abstractmethod
    async def reset_user(self, user_input: UserResetDTO, user: UserContextDTO) -> UserDTO:
        """
        Повторно регистрирует пользователя.

        Основные аспекты:
        - Пользователь должен существовать до повторной регистрации.
        - Номер телефона пользователя должен соответствовать ранее установленному или быть уникальным.
        - Повторная регистрация требует подтверждения Администратора.

        Args:
            user_input (UserResetDTO): Объект класса пользователя, производного от `UserResetDTO`, соответствующий полю `role` класса `UserResetDTO`.
            user (UserContextDTO)

        Returns:
            UserDTO: Объект класса пользователя, соответствующий роли повторно зарегистрированного пользователя.

        Raises:
            DuplicateEntryException: Возникает, если контактные данные пользователя (например, номер телефона) уже используются другим пользователем.
            IntegrityException: Возникает при нарушении целостности данных.
        """
        pass