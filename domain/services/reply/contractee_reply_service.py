from typing import List
from abc import ABC, abstractmethod

from domain.entities import Contractee

from domain.dto.input import ReplyInputDTO
from domain.dto.common import ReplyDTO, DetailedReplyDTO

class ContracteeReplyService(ABC):
    """
    Интерфейс для сервисов откликов исполнителя.
    
    Этот класс определяет интерфейс для сервисов, отвечающих за возможности исполнителя по управлению откликами.
    """

    @abstractmethod
    async def submit_reply_to_order(self, reply_input: ReplyInputDTO, contractee: Contractee) -> DetailedReplyDTO:
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
            DetailedReplyDTO: DTO с данными созданного отклика.
        
        Raises:
            InvalidReplyException: Возникает, если отклик не может быть отправлен.
            IntegrityException: Возникает при нарушении целостности данных.
        """
        pass

    @abstractmethod
    async def get_reply(self, contractee_id: int, detail_id: int, contractee: Contractee) -> DetailedReplyDTO | None:
        """
        Получает отклик.
        
        Args:
            contractee_id (int): ID исполнителя.
            detail_id (int): ID позиции.
            contractee (Contractee): Объект исполнителя.

        Returns:
            DetailedReplyDTO: DTO с данными отклика. Может быть `None`, если был запрошен чужой отклик или отклика не существует.
        """
        pass

    @abstractmethod
    async def get_replies(self, contractee: Contractee, page: int = 1, size: int = 10) -> List[DetailedReplyDTO]:
        """
        Получает список откликов исполнителя по его ID.
        
        Args:
            contractee (Contractee): Объект исполнителя.
            page (int): Номер страницы.
            size (int): Размер страницы. По умолчанию размер страницы равен 10.

        Returns:
            List[DetailedReplyDTO]: Список DTO с данными откликов.
        """
        pass

    @abstractmethod
    async def get_approved_replies(self, contractee: Contractee, page: int = 1, size: int = 10) -> List[DetailedReplyDTO]:
        """
        Получает список неподтвержденных откликов исполнителя по его ID.
        
        Args:
            contractee (Contractee): Объект исполнителя.
            page (int): Номер страницы.
            size (int): Размер страницы. По умолчанию размер страницы равен 10.

        Returns:
            List[DetailedReplyDTO]: Список DTO с данными откликов.
        """
        pass

    @abstractmethod
    async def get_unapproved_replies(self, contractee: Contractee, page: int = 1, size: int = 10) -> List[DetailedReplyDTO]:
        """
        Получает список неподтвержденных откликов исполнителя по его ID.
        
        Args:
            contractee (Contractee): Объект исполнителя.
            page (int): Номер страницы.
            size (int): Размер страницы. По умолчанию размер страницы равен 10.

        Returns:
            List[DetailedReplyDTO]: Список DTO с данными откликов.
        """
        pass

    