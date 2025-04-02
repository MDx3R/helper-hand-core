from abc import ABC, abstractmethod

from domain.dto.common import ContracteeDTO, ContractorDTO

from domain.dto.internal import ResetDTO

class UserResetService(ABC):
    """
    Интерфейс для сервисов повторной регистрации пользователей.
    """
    @abstractmethod
    async def reset_user(self, request: ResetDTO) -> ContracteeDTO | ContractorDTO:
        """
        Повторно регистрирует пользователя.

        Основные аспекты:
        - Пользователь должен существовать до повторной регистрации.
        - Номер телефона пользователя должен соответствовать ранее установленному или быть уникальным.
        - Повторная регистрация требует подтверждения Администратора.

        Raises:
            PermissionDeniedException
            DuplicateEntryException
            IntegrityException
        """
        pass