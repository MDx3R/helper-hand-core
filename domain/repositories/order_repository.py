from typing import List
from abc import ABC, abstractmethod

from domain.models import Order, DetailedOrder, Contractor
from domain.models.enums import OrderStatusEnum

class OrderRepository(ABC):
    @abstractmethod
    async def get_order_by_id(self, order_id: int) -> Order | None:
        """
        Получает заказ по его ID.
        
        Args:
            order_id (int): ID заказа.

        Returns:
            Order: Модель с данными заказа или `None`, если заказ не найден.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_order_by_detail_id(self, detail_id: int) -> Order | None:
        """
        Получает заказ по ID его позиции.
        
        Args:
            detail_id (int): ID позиции.

        Returns:
            Order: Модель с данными заказа или `None`, если заказ не найден.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_order_by_id_and_contractor_id(self, order_id: int, contractor_id: int) -> Order | None:
        """
        Получает заказ по его ID и ID заказчика.
        
        Args:
            order_id (int): ID заказа.
            contractor_id (int): ID заказчика.

        Returns:
            Order: Модель с данными заказа или `None`, если заказ не найден.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_detailed_order_by_id(self, order_id: int) -> DetailedOrder | None:
        """
        Получает заказ и сведения о нем по его ID.
        
        Args:
            order_id (int): ID заказа.

        Returns:
            DetailedOrder: Модель с данными заказа и сведениями о нем или `None`, если заказ не найден.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_detailed_order_by_id_and_contractor_id(self, order_id: int, contractor_id: int) -> DetailedOrder | None:
        """
        Получает заказ и сведения о нем по его ID и ID заказчика.
        
        Args:
            order_id (int): ID заказа.
            contractor_id (int): ID заказчика.

        Returns:
            DetailedOrder: Модель с данными заказа и сведениями о нем или `None`, если заказ не найден.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_detailed_open_orders_by_page(self, page: int = 1, size: int = None) -> List[DetailedOrder]:
        """
        Получает открытые заказы и сведения о них постранично.
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала.
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.

        Args:
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[DetailedOrder]: Список открытых заказов вместе со сведениями о них. Результат может быть пустым, если заказы не найдены.

        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_detailed_open_orders_by_last_order_id(self, last_order_id: int = None, size: int = None) -> List[DetailedOrder]:
        """
        Получает открытые заказы и сведения о них, ID которых больше `last_order_id`.
        На основе параметра `size` рассчитывается `limit` (`limit = size`).
        Если параметр `last_order_id` равен `None`, то элементы берутся с начала.
        Если параметр `size` равен `None`, то возвращаются все элементы после заказа с ID `last_order_id`.

        Args:
            last_order_id (int): ID последнего заказа.
            size (int): количество элементов на возврат.

        Returns:
            List[DetailedOrder]: Список открытых заказов вместе со сведениями о них. Результат может быть пустым, если заказы не найдены.

        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_contractor_by_order_id(self, order_id: int) -> Contractor | None:
        """
        Получает заказчика по ID заказа.
        
        Args:
            order_id (int): ID заказа.

        Returns:
            Contractor: Модель заказчика.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_contractor_orders_by_page(self, contractor_id: int, page: int = 1, size: int = None) -> List[Order]:
        """
        Получает заказы по ID заказчика постранично. 
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.
        
        Args:
            contractor_id (int): ID заказчика.
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[Order]: Список заказов. Результат может быть пустым, если заказы не найдены. 
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_contractor_orders_by_last_order_id(self, contractor_id: int, last_order_id: int = None, size: int = None) -> List[Order]:
        """
        Получает заказы, ID который больше `last_order_id`, по ID заказчика. 
        На основе параметра `size` рассчитывается `limit` (`limit = size`).
        Если параметр `last_order_id` равен `None`, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после заказа с ID `last_order_id`.

        Args:
            contractor_id (int): ID заказчика.
            last_order_id (int): ID последнего заказа.
            size (int): количество элементов на возврат.

        Returns:
            List[Order]: Список заказов. Результат может быть пустым, если заказы не найдены. 
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_contractor_detailed_orders_by_page(self, contractor_id: int, page: int = 1, size: int = None) -> List[DetailedOrder]:
        """
        Получает заказы и сведения о них по ID заказчика постранично. 
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.
        
        Args:
            contractor_id (int): ID заказчика.
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[DetailedOrder]: Список заказов вместе со сведениями о них. Результат может быть пустым, если заказы не найдены. 
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_contractor_detailed_orders_by_last_order_id(self, contractor_id: int, last_order_id: int = None, size: int = None) -> List[DetailedOrder]:
        """
        Получает заказы и сведения о них, ID который больше `last_order_id`, по ID заказчика. 
        На основе параметра `size` рассчитывается `limit` (`limit = size`).
        Если параметр `last_order_id` равен `None`, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после заказа с ID `last_order_id`.

        Args:
            contractor_id (int): ID заказчика.
            last_order_id (int): ID последнего заказа.
            size (int): количество элементов на возврат.

        Returns:
            List[DetailedOrder]: Список заказов вместе со сведениями о них. Результат может быть пустым, если заказы не найдены. 
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_admin_orders_by_page(self, admin_id: int, page: int = 1, size: int = None) -> List[Order]:
        """
        Получает заказы, курируемых администратором, по его ID постранично. 
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.
        
        Args:
            admin_id (int): ID заказчика.
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[Order]: Список заказов. Результат может быть пустым, если заказы не найдены. 
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_admin_orders_by_last_order_id(self, admin_id: int, last_order_id: int = None, size: int = None) -> List[Order]:
        """
        Получает курируемых администратором заказы, ID которых больше `last_order_id`, по ID администратора. 
        На основе параметра `size` рассчитывается `limit` (`limit = size`).
        Если параметр `last_order_id` равен `None`, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после заказа с ID `last_order_id`.
        
        Args:
            admin_id (int): ID заказчика.
            last_order_id (int): ID последнего заказа.
            size (int): количество элементов на странице.

        Returns:
            List[Order]: Список заказов. Результат может быть пустым, если заказы не найдены. 
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_contractee_orders_by_page(self, contractee_id: int, page: int = 1, size: int = None) -> List[Order]:
        """
        Получает заказы по ID исполнителя постранично.
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала.
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.

        Args:
            contractee_id (int): ID исполнителя.
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[Order]: Список заказов. Результат может быть пустым, если заказы не найдены.

        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_contractee_orders_by_last_order_id(self, contractee_id: int, last_order_id: int = None, size: int = None) -> List[Order]:
        """
        Получает заказы, ID которых больше `last_order_id`, по ID исполнителя.
        На основе параметра `size` рассчитывается `limit` (`limit = size`).
        Если параметр `last_order_id` равен `None`, то элементы берутся с начала.
        Если параметр `size` равен `None`, то возвращаются все элементы после заказа с ID `last_order_id`.

        Args:
            contractee_id (int): ID исполнителя.
            last_order_id (int): ID последнего заказа.
            size (int): количество элементов на возврат.

        Returns:
            List[Order]: Список заказов. Результат может быть пустым, если заказы не найдены.

        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def save_order(self, order: Order) -> Order:
        """
        Сохраняет заказ.

        Args:
            order (Order): объект заказа.

        Returns:
            Order: Созданный заказ.

        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных.
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def change_order_status(self, order_id: int, status: OrderStatusEnum) -> Order:
        """
        Изменяет статус заказа.
        
        Args:
            order_id (int): ID заказа.
            status (OrderStatusEnum): новый статус заказа.
            
        Returns:
            Order: Изменённый заказ.

        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных.
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_orders_by_page(self, page: int = 1, size: int = None) -> List[Order]:
        """
        Получает заказы постранично. 
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.
        
        Args:
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[Order]: Список заказов.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_detailed_orders_by_page(self, page: int = 1, size: int = None) -> List[DetailedOrder]:
        """
        Получает заказы и сведения о них постранично. 
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.
        
        Args:
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[DetailedOrder]: Список заказов вместе с их сведениями.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_open_orders_by_page(self, page: int = 1, size: int = None) -> List[Order]:
        """
        Получает открытые заказы и сведения о них постранично. 
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.
        
        Args:
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[Order]: Список заказов.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_closed_orders_by_page(self, page: int = 1, size: int = None) -> List[Order]:
        """
        Получает закрытые заказы и сведения о них постранично. 
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.
        
        Args:
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[Order]: Список заказов.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_active_orders_by_page(self, page: int = 1, size: int = None) -> List[Order]:
        """
        Получает активные заказы и сведения о них постранично.
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.
        
        Args:
            page (int): номер страницы.
            size (int): количество элементов на странице.

        Returns:
            List[Order]: Список заказов.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_detailed_unassigned_orders_by_page(self, page: int = 1, size: int = None) -> List[DetailedOrder]:
        """
        Получает неприкрепленные к администратору заказы и сведения о них, ID которых больше `last_order_id`.
        На основе параметров `page` и `size` рассчитывается `offset` (`offset = (page-1)*size`) и `limit` (`limit = size`).
        Если параметр `page` равен 1, то элементы берутся с начала. 
        Если параметр `size` равен `None`, то возвращаются все элементы после отступа.

        Args:
            page (int): номер страницы.
            size (int): количество элементов на возврат.

        Returns:
            List[DetailedOrder]: Список открытых заказов вместе со сведениями о них. Результат может быть пустым, если заказы не найдены.

        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_detailed_unassigned_orders_by_last_order_id(self, last_order_id: int = None, size: int = None) -> List[DetailedOrder]:
        """
        Получает неприкрепленные к администратору заказы и сведения о них, ID которых больше `last_order_id`.
        На основе параметра `size` рассчитывается `limit` (`limit = size`).
        Если параметр `last_order_id` равен `None`, то элементы берутся с начала.
        Если параметр `size` равен `None`, то возвращаются все элементы после заказа с ID `last_order_id`.

        Args:
            last_order_id (int): ID последнего заказа.
            size (int): количество элементов на возврат.

        Returns:
            List[DetailedOrder]: Список открытых заказов вместе со сведениями о них. Результат может быть пустым, если заказы не найдены.

        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass