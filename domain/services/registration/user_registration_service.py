from abc import ABC, abstractmethod

from domain.dto.input import UserInputDTO
from domain.dto.common import UserDTO

class UserRegistrationService(ABC):
    """
    Интерфейс для сервисов регистрации пользователей.
    """
    @abstractmethod
    async def register_user(self, user_input: UserInputDTO) -> UserDTO:
        """
        Регистрирует нового пользователя.

        Основные аспекты:
        - Пользователь не должен существовать до регистрации.
        - Номер телефона пользователя должен быть уникальным.
        - Регистрация требует подтверждения Администратора.
        - Регистрация пользователей из источника, отличного от Telegram,
          требует дополнительно подтверждения из Telegram самим пользователей. 
          Уведомление администраторам отправляется после такого подтверждения.

        Args:
            user_input (UserInputDTO): Объект класса пользователя, производного от `UserInputDTO`, соответствующий полю `role` класса `UserInputDTO`.

        Returns:
            UserDTO: Объект класса пользователя, соответствующий роли зарегистрированного пользователя.

        Raises:
            DuplicateEntryException: Возникает, если контактные данные пользователя (например, номер телефона) уже используются другим пользователем.
            IntegrityException: Возникает при нарушении целостности данных.
        """
        pass