from typing import List
from abc import ABC, abstractmethod

from domain.entities import OrderDetail

class OrderDetailRepository(ABC):
    @abstractmethod
    async def get_detail_by_id(self, detail_id: int) -> OrderDetail | None:
        """
        Получает сведения о заказе по их ID.
        
        Args:
            detail_id (int): ID сведений о заказе.
            
        Returns:
            OrderDetail: Модель с данными сведений о заказе или `None`, если сведения не найдены.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_details_by_order_id(self, detail_id: int) -> OrderDetail | None:
        """
        Получает сведения о заказе по их ID.
        
        Args:
            detail_id (int): ID сведений о заказе.
            
        Returns:
            OrderDetail: Модель с данными сведений о заказе или `None`, если сведения не найдены.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def save_detail(self, detail: OrderDetail) -> OrderDetail:
        """
        Сохраняет один экземпляр сведения о заказе.
        
        Args:
            detail (OrderDetail): сведения о заказе. В объекте должен быть указан `order_id`.
            
        Returns:
            OrderDetail: Созданные сведения о заказе.

        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных.
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def save_details(self, details: List[OrderDetail]) -> List[OrderDetail]:
        """
        Сохраняет несколько экземпляров сведений о заказе.
        
        Args:
            details (List[OrderDetail]): список сведений о заказе. В объектах должен быть указан `order_id`.
            
        Returns:
            List[OrderDetail]: Список созданных сведений о заказе.

        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных.
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass
    
    @abstractmethod
    async def create_details(self, details: List[OrderDetail]) -> List[OrderDetail]:
        """
        Создает несколько экземпляров сведений о заказе. 
        В отличии от `save_details` в результате выполнения всегда добавляются новые записи.
        
        Args:
            details (List[OrderDetail]): список сведений о заказе. В объектах должен быть указан `order_id`.
            
        Returns:
            List[OrderDetail]: Список созданных сведений о заказе.

        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных.
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_available_details_by_order_id(self, order_id: int) -> List[OrderDetail]:
        """
        Получает сведения о заказе, имеющие свободные места, по ID заказа.
        
        Args:
            order_id (int): ID заказа.

        Returns:
            List[OrderDetail]: Список доступных сведений о заказе. Результат может быть пустым, если сведения не найдены.
            
        Raises:
            RepositoryException: При всех непредвиденных ошибках.
        """
        pass