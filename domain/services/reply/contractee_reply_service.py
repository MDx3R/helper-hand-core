from typing import List
from abc import ABC, abstractmethod

from domain.models import Contractee

from application.dtos.input import ReplyInputDTO
from application.dtos.output import ReplyOutputDTO, DetailedReplyOutputDTO

class ContracteeReplyService(ABC):
    """
    Интерфейс для сервисов откликов исполнителя.
    
    Этот класс определяет интерфейс для сервисов, отвечающих за возможности исполнителя по управлению откликами.
    """

    @abstractmethod
    async def submit_reply_to_order(self, reply_input: ReplyInputDTO, contractee: Contractee) -> DetailedReplyOutputDTO:
        """
        Создает новый отклик на заказ.

        Основные аспекты:
        - Отклик исполнителя на заказ требует подтверждения заказчиком.
        - Отклик может быть отправлен только на открытый заказ.
        - Отклик может быть отправлен только на позицию, для которой есть свободные места.
        - Отклик не может быть отправлен повторно.
        - Отклик не может быть отправлен на дату, которая уже прошла или которая занята другим подтвержденным откликом.
        - На одну дату может быть отправлено много откликов. Подтверждается только один.
        - После успешного создания отклика отправляется уведомление заказчику.
        
        Args:
            reply_input (ReplyInputDTO): DTO с данными для создания отклика.
        
        Returns:
            DetailedReplyOutputDTO: DTO с данными созданного отклика.
        
        Raises:
            InvalidReplyException: Возникает, если отклик не может быть отправлен.
            IntegrityException: Возникает при нарушении целостности данных.
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках в процессе создания отклика.
        """
        pass

    @abstractmethod
    async def get_replies(self, contractee: Contractee) -> List[DetailedReplyOutputDTO]:
        """
        Получает список откликов исполнителя по его ID.
        
        Args:
            contractee (Contractee): Объект исполнителя.

        Returns:
            List[DetailedReplyOutputDTO]: Список DTO с данными откликов.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_unapproved_replies(self, contractee: Contractee) -> List[DetailedReplyOutputDTO]:
        """
        Получает список неподтвержденных откликов исполнителя по его ID.
        
        Args:
            contractee (Contractee): Объект исполнителя.

        Returns:
            List[DetailedReplyOutputDTO]: Список DTO с данными откликов.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    