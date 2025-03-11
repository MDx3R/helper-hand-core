from typing import List
from abc import ABC, abstractmethod

from datetime import datetime

from domain.models import Reply, DetailedReply, AvailableRepliesForDetail, Contractee
from domain.models.enums import ReplyStatusEnum

class ReplyRepository(ABC):
    @abstractmethod
    async def get_reply(self, contractee_id: int, detail_id: int) -> Reply | None:
        """
        Получает отклик по ID исполнителя и сведений о заказе.
        
        Args:
            contractee_id (int): ID исполнителя.
            detail_id (int): ID заказа.

        Returns:
            Reply: Отклик. Может быть `None`, если отклик не найден.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_detailed_reply(self, contractee_id: int, detail_id: int) -> DetailedReply | None:
        """
        Получает подробный отклик по ID исполнителя и сведений о заказе. 
        
        Результат метода включает в себя отклик, сведения, заказ и исполнителя. 
        
        Args:
            contractee_id (int): ID исполнителя.
            detail_id (int): ID заказа.

        Returns:
            DetailedReply: Отклик. Может быть `None`, если отклик не найден.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_replies_by_contractee_id(self, contractee_id: int) -> List[DetailedReply]:
        """
        Получает список откликов исполнителя по его ID.

        Args:
            contractee_id (int): ID исполнителя.
        
        Returns:
            List[DetailedReply]: Список откликов. Может быть пустым, если отклики не найдены.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_approved_replies_by_contractee_id(self, contractee_id: int) -> List[DetailedReply]:
        """
        Получает список подтвержденных откликов исполнителя по его ID.

        Args:
            contractee_id (int): ID исполнителя.
        
        Returns:
            List[DetailedReply]: Список откликов. Может быть пустым, если отклики не найдены.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_unapproved_replies_by_contractee_id(self, contractee_id: int) -> List[DetailedReply]:
        """
        Получает список неподтвержденных откликов исполнителя по его ID.

        Args:
            contractee_id (int): ID исполнителя.
        
        Returns:
            List[DetailedReply]: Список откликов. Может быть пустым, если отклики не найдены.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_approved_contractees_by_order_id(self, order_id: int) -> List[Contractee]:
        """
        Получает список подтвержденных исполнителей по ID заказа.

        Args:
            order_id (int): ID заказа.
        
        Returns:
            List[Contractee]: Список заказов. Может быть пустым, если отклики не найдены.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_approved_replies_count_by_detail_id(self, detail_id: int) -> int:
        """
        Получает **количество** подтвержденных откликов на сведения о заказе по его ID.
        
        Args:
            detail_id (int): ID сведений о заказе.
        
        Returns:
            int: Количество подтвержденных откликов. Принимает неотрицательные значения.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_approved_replies_count_by_order_id(self, order_id: int) -> int:
        """
        Получает **количество** подтвержденных откликов на заказ о заказе по его ID.
        
        Args:
            order_id (int): ID заказа.
        
        Returns:
            int: Количество подтвержденных откликов. Принимает неотрицательные значения.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_available_replies_count_by_detail_id(self, detail_id: int) -> int:
        """
        Считает **количество** свободных мест на сведения о заказе по его ID.
        
        Args:
            detail_id (int): ID сведений о заказе.
        
        Returns:
            int: Количество свободных мест. Принимает неотрицательные значения.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_available_replies_count_by_order_id(self, order_id: int) -> int:
        """
        Считает **количество** свободных мест на заказ по его ID.
        
        Args:
            order_id (int): ID заказа.

        Returns:
            int: Количество свободных мест. Принимает неотрицательные значения.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_available_replies_count_for_details_by_order_id(self, order_id: int) -> List[AvailableRepliesForDetail]:
        """
        Получает количество свободных мест на каждую позицию заказе по его ID.
        
        Args:
            order_id (int): ID заказа
        
        Returns:
            List[AvailableRepliesForDetail]: Список объектов, каждый из которых содержит:
                - detail_id (int): ID сведений о заказе.
                - quantity (int): Количество свободных мест.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def save_reply(self, reply: Reply) -> Reply:
        """
        Создает отклик.
        
        Args:
            reply (Reply): Отклик.

        Returns:
            Reply: Созданный отклик.

        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных. Если произошло нарушение целостности данных.
            DuplicateEntryException: Возникает, если уникальные значения повторяются. Если отклик уже существует.
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def change_reply_status(self, contractee_id: int, detail_id: int, status: ReplyStatusEnum) -> Reply:
        """
        Изменяет статус отклика по его ID.
        
        Args:
            reply_id (int): ID отклика.
            status (str): Новый статус отклика.

        Returns:
            Reply: Измененный отклик.

        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных. Если произошло нарушение целостности данных.
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def drop_order_replies_by_order_id(self, order_id: int) -> List[Contractee]:
        """
        Отклоняет все отклики на заказ по его ID.
        
        Args:
            order_id (int): ID заказа.

        Returns:
            List[Contractee]: Список исполнителей, чьи отклики были отклонены. Может быть пустым, если отклики не найдены.

        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных. Если произошло нарушение целостности данных.
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def drop_unapproved_order_replies_by_order_id(self, order_id: int) -> List[Contractee]:
        """
        Отклоняет все неподтвержденные отклики на заказ по его ID.
        
        См. также `drop_unapproved_order_detail_replies_by_detail_id`.
        Для отклонения неподтвержденные откликов по ID сведений используется метод `drop_unapproved_order_detail_replies_by_detail_id`.

        Args:
            order_id (int): ID заказа.

        Returns:
            List[Contractee]: Список исполнителей, чьи отклики были отклонены. Может быть пустым, если отклики не найдены.

        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных. Если произошло нарушение целостности данных.
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def drop_unapproved_order_detail_replies_by_detail_id(self, detail_id: int) -> List[Contractee]:
        """
        Отклоняет все неподтвержденные отклики на сведения о заказе по его ID.
        
        См. также `drop_unapproved_order_replies_by_order_id`.
        Для отклонения неподтвержденные откликов по ID заказа используется метод `drop_unapproved_order_replies_by_order_id`.

        Args:
            order_id (int): ID заказа.

        Returns:
            List[Contractee]: Список исполнителей, чьи отклики были отклонены. Может быть пустым, если отклики не найдены.

        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных. Если произошло нарушение целостности данных.
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def drop_contractee_unapproved_replies_by_date(self, contractor_id: int, date: datetime) -> None:
        """
        Отклоняет все неподтвержденные отклики исполнителя для указанной даты.
        
        Args:
            contractor_id (int): ID исполнителя.
            date (datetime): Дата, на которой отклоняются отклики.

        Returns:
            None

        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_first_unapproved_reply_by_contractor_id(self, contractor_id: int) -> DetailedReply | None:
        """
        Получает первый неподтвержденный отклик для заказов по ID заказчика.
        
        Args:
            contractor_id (int): ID заказчика.
            
        Returns:
            DetailedReply: Неподтвержденный отклик или `None`, если неподтвержденный отклик не найден.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_first_unapproved_reply_by_order_id(self, order_id: int) -> DetailedReply | None:
        """
        Получает первый неподтвержденный отклик для заказа по его ID.
        
        Args:
            order_id (int): ID заказа.
            
        Returns:
            DetailedReply: Неподтвержденный отклик или `None`, если неподтвержденный отклик не найден.
                        Поле `order` устанавливается как `None`.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_first_unapproved_reply_by_order_id_and_contractor_id(self, order_id: int, contractor_id: int) -> DetailedReply | None:
        """
        Получает первый неподтвержденный отклик для заказа по его ID и ID заказчика.
        
        Args:
            order_id (int): ID заказа.
            contractor_id (int): ID заказчика.
            
        Returns:
            DetailedReply: Неподтвержденный отклик или `None`, если неподтвержденный отклик не найден.
                        Поле `order` устанавливается как `None`.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass
    
    @abstractmethod
    async def get_unapproved_replies_by_order_id_by_page(self, order_id: int, page: int = 1, size: int = None) -> List[DetailedReply]:
        """
        Получает список неподтвержденных откликов на заказ по его ID постранично. 
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.

        Args:
            order_id (int): ID заказа.
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[DetailedReply]: Список неподтвержденных откликов для заказа. 
                        Поле `order` устанавливается как `None`.
                        Результат может быть пустым, если неподтвержденные отклики не найдены. 
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_unapproved_replies_by_order_id_and_contractor_id_by_page(self, order_id: int, contractor_id: int, page: int = 1, size: int = None) -> List[DetailedReply]:
        """
        Получает список неподтвержденных откликов на заказ по его ID и ID заказчика постранично. 
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.

        Args:
            order_id (int): ID заказа.
            contractor_id (int): ID заказчика.
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[DetailedReply]: Список неподтвержденных откликов для заказа. 
                        Поле `order` устанавливается как `None`.
                        Результат может быть пустым, если неподтвержденные отклики не найдены.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass
    
    @abstractmethod
    async def get_approved_replies_by_order_id_by_page(self, order_id: int, page: int = 1, size: int = None) -> List[DetailedReply]:
        """
        Получает список подтвержденных откликов на заказ по его ID постранично. 
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.

        Args:
            order_id (int): ID заказа.
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[DetailedReply]: Список подтвержденных откликов для заказа. 
                        Поле `order` устанавливается как `None`.
                        Результат может быть пустым, если подтвержденные отклики не найдены. 
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_approved_replies_by_order_id_and_contractor_id_by_page(self, order_id: int, contractor_id: int, page: int = 1, size: int = None) -> List[DetailedReply]:
        """
        Получает список подтвержденных откликов на заказ по его ID и ID заказчика постранично. 
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.

        Args:
            order_id (int): ID заказа.
            contractor_id (int): ID заказчика.
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[DetailedReply]: Список подтвержденных откликов для заказа. 
                        Поле `order` устанавливается как `None`.
                        Результат может быть пустым, если подтвержденные отклики не найдены. 
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def is_contractee_busy_on_date(self, contractee_id: int, date: datetime) -> bool:
        """
        Проверяет, есть ли у исполнителя отклик на указанную дату.

        Args:
            contractee_id (int): ID исполнителя.
            date (datetime): Дата для проверки.

        Returns:
            bool: `True`, если у исполнителя есть отклик на указанную дату, иначе `False`.

        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_contractee_approved_future_busy_dates(self, contractee_id: int) -> List[datetime]:
        """
        Возвращает все занятые дни исполнителя после настоящего времени. 
        Даты возвращаются только для позиций, отклики на которые были подтверждены.

        Args:
            contractee_id (int): ID исполнителя.

        Returns:
            List[datetime]

        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_contractee_future_replies(self, contractee_id: int) -> List[Reply]:
        """
        Возвращает список всех откликов на позиции, начинающихся после настоящего времени.

        Args:
            contractee_id (int): ID исполнителя.

        Returns:
            List[Reply]

        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def has_contractee_replied_to_order(self, order_id: int, contractee_id: int) -> bool:
        """
        Проверяет, есть ли у исполнителя отклик на заказ.

        Args:
            order_id (int): ID заказа.
            contractee_id (int): ID исполнителя.

        Returns:
            bool: `True`, если у исполнителя есть отклик на заказ, иначе `False`.

        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass