from typing import List
from abc import ABC, abstractmethod

from domain.entities import Contractor

from domain.dto.common import DetailedReplyDTO

class ContractorReplyService(ABC):
    """
    Абстрактный класс для сервисов откликов заказчика.

    Этот класс определяет интерфейс для сервисов, отвечающих за возможности заказчика по управлению откликами.
    """

    @abstractmethod
    async def get_first_unapproved_reply(self, contractor: Contractor) -> DetailedReplyDTO | None:
        """
        Получает первый неподтвержденный отклик, требующий подтверждения заказчика.

        Args:
            contractor (Contractor): Объект заказчика.
            
        Returns:
            DetailedReplyDTO: DTO с подробными данными отклика или `None`, если отклик не найден.

        Raises:
            Exception: Если произошла ошибка при получении списка заказов.
        """
        pass

    @abstractmethod
    async def get_first_unapproved_reply_for_order(self, order_id: int, contractor: Contractor) -> DetailedReplyDTO | None:
        """
        Получает первый неподтвержденный отклик на заказ по его ID.

        Args:
            order_id (int): ID заказа.
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему заказам.
            
        Returns:
            DetailedReplyDTO: DTO с подробными данными отклика. 
            Может быть `None`, если отклик не найден. 

        Raises:
            Exception: Если произошла ошибка при получении списка заказов.
        """
        pass

    @abstractmethod
    async def get_unapproved_replies_for_order(self, order_id: int, contractor: Contractor, page: int = 1, size: int = 20) -> List[DetailedReplyDTO]:
        """
        Получает список неподтвержденных откликов на заказ по его ID.

        Args:
            order_id (int): ID заказа.
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему заказам.
            page (int): номер страницы.
            size (int): размер страницы. По умолчанию размер страницы равен 20.
            
        Returns:
            List[DetailedReplyDTO]: DTO с подробными данными отклика. 

        Raises:
            Exception: Если произошла ошибка при получении списка заказов.
        """
        pass

    @abstractmethod
    async def get_approved_replies_for_order(self, order_id: int, contractor: Contractor, page: int = 1, size: int = 20) -> List[DetailedReplyDTO]:
        """
        Получает список подтвержденных откликов на заказ по его ID.

        Args:
            order_id (int): ID заказа.
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему заказам.
            page (int): номер страницы.
            size (int): размер страницы. По умолчанию размер страницы равен 20.
            
        Returns:
            List[DetailedReplyDTO]: DTO с подробными данными отклика. 

        Raises:
            Exception: Если произошла ошибка при получении списка заказов.
        """
        pass

    @abstractmethod
    async def approve_reply(self, contractee_id: int, detail_id: int, contractor: Contractor) -> DetailedReplyDTO | None:
        """
        Подтверждает отклик по его ID.

        Основные аспекты отмены заказа:
        - Отклик может быть подтвержден только для открытого заказа.
        - Отклик может быть подтвержден, только если его статус установлен как `ReplyStatusEnum.created`.
        - Отклик может быть подтвержден только позиции, для которой есть свободные места.
        - Все отклики исполнителя на туже дату отменяются.
        - Если после подтверждения отклика на позиции не осталось свободных мест, то все неподтверждённые отклики отменяются автоматически. 
        Владельцы отмененных откликов получают соответствующие уведомления.
        - Если после подтверждения отклика на заказ не осталось свободных мест, заказчик и администратор получают соответствующее уведомление. 
        Заказ автоматически закрывается. Все неподтверждённые отклики отменяются автоматически. Владельцы отмененных откликов получают соответствующие уведомления.
        - После успешного подтверждения отклика отправляется уведомление исполнителю.

        Args:
            reply_id (int): ID отклика.
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему откликам.

        Returns:
            DetailedReplyDTO: DTO с подробными данными отклика.

        Raises:
            Exception: Если произошла ошибка при подтверждении отклика.
        """
        pass

    @abstractmethod
    async def disapprove_reply(self, contractee_id: int, detail_id: int, contractor: Contractor) -> DetailedReplyDTO | None:
        """
        Отклоняет отклик по его ID.

        Args:
            reply_id (int): ID отклика.
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему откликам.

        Returns:
            DetailedReplyDTO: DTO с подробными данными отклика.

        Raises:
            Exception: Если произошла ошибка при отклонении отклика.
        """
        pass
