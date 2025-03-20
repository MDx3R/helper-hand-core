from abc import abstractmethod

from .user_registration_service import UserRegistrationService
from domain.dto.input import ContractorInputDTO
from domain.dto.output import ContractorOutputDTO

class ContractorRegistrationService(UserRegistrationService):
    """
    Расширение интерфейса `UserRegistrationService` для сервисов регистрации заказчиков.
    
    Этот класс определяет интерфейс для сервисов, отвечающих за регистрацию новых заказчиков.
    """

    @abstractmethod
    async def register_user(self, user_input: ContractorInputDTO) -> ContractorOutputDTO:
        """
        Регистрирует нового заказчика.

        Основные аспекты:
        - Регистрация требует подтверждения Администратора.
        - Номер телефона пользователя должен быть уникальным.
        - Поддерживается возможность перерегистрации пользователя в случае сброса его учетной записи Администратором.
        - После успешной регистрации отправляется уведомление администраторам.

        Args:
            user_input (ContractorInputDTO): DTO с данными для регистрации заказчика, включая имя, фамилию, номер телефона и другие необходимые данные.

        Returns:
            ContractorOutputDTO: DTO с данными зарегистрированного заказчика, включая уникальный идентификатор и статус регистрации.

        Raises:
            AlreadyAuthenticatedException: Возникает, если пользователь уже аутентифицирован и пытается повторно зарегистрироваться.
            UserBlockedException: Возникает, если пользователь заблокирован.
            DuplicateEntryException: Возникает, если контактные данные пользователя (например, номер телефона) уже используются другим пользователем.
            IntegrityException: Возникает при нарушении целостности данных.
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках в процессе регистрации.
        """
        pass