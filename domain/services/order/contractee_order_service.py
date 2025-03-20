from typing import List
from abc import ABC, abstractmethod

from domain.entities import Contractee

from application.dtos.output import DetailedOrderOutputDTO, OrderOutputDTO, OrderDetailOutputDTO

class ContracteeOrderService(ABC):
    """
    Интерфейс для сервисов заказов исполнителя.

    Этот класс определяет интерфейс для сервисов, отвечающих за возможности исполнителя по работе с заказами.
    """
    
    @abstractmethod
    async def get_order(self, order_id: int, contractee: Contractee) -> DetailedOrderOutputDTO | None:
        """
        Получает заказ по его ID.

        Исполнителю доступны только следующие заказы:
        - все открытые заказы
        - все заказы, на которые он отправил отклик.

        Args:
            order_id (int): ID заказа.

        Returns:
            DetailedOrderOutputDTO: DTO с данными заказа.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках в процессе получения заказа.
        """
        pass

    @abstractmethod
    async def get_one_open_order(self, contractee: Contractee, last_order_id: int = None) -> DetailedOrderOutputDTO | None:
        """
        Получает открытый заказ.

        Если `last_order_id` равен `None`, возвращается первый открытый заказ. Иначе, первый открытый заказ после `last_order_id`.

        Args:
            contractee (Contractee): Объект исполнителя.
            last_order_id (int): ID последнего запрошенного заказа.

        Returns:
            DetailedOrderOutputDTO: DTO с данными открытого заказа.

        Raises:
            Exception: Если произошла ошибка при получении открытого заказа.
        """
        pass

    @abstractmethod
    async def get_open_orders(self, contractee: Contractee, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        """
        Получает все открытые заказы постранично.

        Args:
            contractee (Contractee): Объект исполнителя.
            page (int): Номер страницы.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[DetailedOrderOutputDTO]: Список DTO с данными открытых заказов.

        Raises:
            Exception: Если произошла ошибка при получении списка открытых заказов.
        """
        pass

    @abstractmethod
    async def get_contractee_orders(self, contractee: Contractee, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        """
        Получает все заказы исполнителя по его объекту постранично.

        Args:
            contractee (Contractee): Объект исполнителя.
            page (int): Номер страницы.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[OrderOutputDTO]: Список DTO с данными заказов исполнителя.

        Raises:
            Exception: Если произошла ошибка при получении списка заказов исполнителя.
        """
        pass

    @abstractmethod
    async def get_available_details(self, order_id: int, contractee: Contractee) -> List[OrderDetailOutputDTO]:
        """
        Получает доступные позиции для исполнителя по ID заказа и объекту исполнителя.

        Args:
            order_id (int): ID заказа.
            contractee (Contractee): Объект исполнителя.

        Returns:
            List[OrderDetailOutputDTO]: Список DTO с данными доступных позиций.

        Raises:
            Exception: Если произошла ошибка при получении доступных позиций.
        """
        pass