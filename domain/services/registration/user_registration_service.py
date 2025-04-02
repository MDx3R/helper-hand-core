from abc import ABC, abstractmethod

from domain.dto.input.registration import UserRegistrationDTO
from domain.dto.common import ContracteeDTO, ContractorDTO

class UserRegistrationService(ABC):
    """
    Интерфейс для сервисов регистрации пользователей.
    """
    @abstractmethod
    async def register_user(self, user_input: UserRegistrationDTO) -> ContracteeDTO | ContractorDTO:
        """
        Регистрирует нового пользователя.

        Основные аспекты:
        - Пользователь не должен существовать до регистрации.
        - Номер телефона пользователя должен быть уникальным.
        - Регистрация требует подтверждения Администратора.
        - Регистрация пользователей из источника, отличного от Telegram,
          требует дополнительно подтверждения из Telegram самим пользователей. 
          Уведомление администраторам отправляется после такого подтверждения.

        Raises:
            DuplicateEntryException
            IntegrityException
        """
        pass