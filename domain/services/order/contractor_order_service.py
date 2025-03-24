from typing import List
from abc import ABC, abstractmethod

from domain.entities import Contractor

from domain.dto.input import OrderInputDTO, OrderDetailInputDTO
from domain.dto.common import DetailedOrderDTO, OrderDTO

class ContractorOrderService(ABC):
    """
    Интерфейс для сервисов заказов заказчика.

    Этот класс определяет интерфейс для сервисов, отвечающих за возможности заказчика по управлению заказами.
    """

    @abstractmethod
    async def create_order(self, order_input: OrderInputDTO, details_input: List[OrderDetailInputDTO], contractor: Contractor) -> DetailedOrderDTO:
        """
        Создает новый заказ.

        Основные аспекты:
        - Создание заказа требует подтверждения администратора.
        - Сведения о заказе (`details_input`) обязательны и не могут отсутствовать.
        - После успешного создание заказа отправляется уведомление администраторам.

        Args:
            order_input (OrderInputDTO): DTO с данными для создания заказа.
            details_input (List[OrderDetailInputDTO]): Список DTO с сведениями заказа. Не может быть пустым.
            

        Returns:
            DetailedOrderDTO: DTO с данными созданного заказа вместе с его сведениями.

        Raises:
            MissingOrderDetailsException: Возникает, если отсутствуют сведения заказа.
            IntegrityException: Возникает при нарушении целостности данных.
        """
        pass
    
    @abstractmethod
    async def get_order(self, order_id: int, contractor: Contractor) -> OrderDTO | None:
        """
        Получает заказ по его ID.

        Заказчик может получить только свои заказы. Параметр `contractor` используется для ограничения доступа заказчика к не принадлежащим ему заказам.

        Args:
            order_id (int): ID заказа.
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему заказам.

        Returns:
            OrderDTO: DTO с данными заказа или `None`, если заказ не найден.
        """
        pass

    @abstractmethod
    async def get_detailed_order(self, order_id: int, contractor: Contractor) -> DetailedOrderDTO | None:
        """
        Получает заказ вместе с его сведениями по его ID.

        Заказчик может получить только свои заказы. Параметр `contractor` используется для ограничения доступа заказчика к не принадлежащим ему заказам.        

        Args:
            order_id (int): ID заказа.
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему заказам.

        Returns:
            DetailedOrderDTO: DTO с данными созданного заказа вместе с его сведениями или `None`, если заказ не найден.
        """
        pass

    @abstractmethod
    async def cancel_order(self, order_id: int, contractor: Contractor) -> OrderDTO:
        """
        Отменяет заказ по его ID: устанавливается статус сброшен (`cancelled`). 

        Основные аспекты отмены заказа:
        - До принятия заказа администратором отмена заказа не отправляет никакие уведомления.
        - До подтверждения заказа администратором отмена оповещает назначенного администратора.
        - После подтверждения заказа администратором отмена заказа отправляет уведомление назначенному администратору и исполнителю соответствующие уведомления. 
        Все отклики отменяются автоматически.
        - Завершенный заказ не может быть отменен.

        Args:
            order_id (int): ID заказа.
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему заказам.

        Raises:
            NotFoundException: Возникает, если заказ не был найден.
            UnauthorizedAccessException: Возникает, если заказчик пытается отменить заказ, который не принадлежит ему.
            OrderStatusChangeNotAllowedException: Возникает, если заказ не может быть отменен.
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def set_order_active(self, order_id: int, contractor: Contractor) -> OrderDTO:
        """
        Закрывает заказ по его ID: устанавливается статус в работе (`active`). 
        Это действие возможно, если для заказа есть хотя бы один подтверждённый отклик, и статус заказа установлен как открытый
        Установка такого статуса уведомляет назначенный администратора, а также всех исполнителей, отправивших отклики, в зависимости от статуса их заявки.
        
        Основные аспекты закрытия заказа:
        - Отмененный, закрытый и завершенный заказ не может быть закрыт.
        - Заказчик может закрыть заказ только после его подтверждения администратором. Закрыть заказ можно только, если есть хотя бы один подтвержденный отклик и статус заказа установлен как открытый.
        - После закрытия отправляется уведомления получают назначенный администратор и подтвержденные и неподтвержденные исполнители, откликнувшиеся на заказ.

        Args:
            order_id (int): ID заказа.
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему заказам.

        Raises:
            NotFoundException: Возникает, если заказ не был найден.
            UnauthorizedAccessException: Возникает, если заказчик пытается закрыть заказ, который не принадлежит ему.
            OrderStatusChangeNotAllowedException: Возникает, если заказ не может быть закрыт.
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_orders(self, contractor: Contractor, page: int = 1, size: int = 15) -> List[OrderDTO]:
        """
        Получает список заказов по ID заказчика.

        Заказчик может получить только свои заказы. Параметр `contractor` используется для ограничения доступа заказчика к не принадлежащим ему заказам.

        Args:
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему заказам.
            page (int): Номер страницы.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[OrderDTO]: Список DTO с заказами заказчика.
        """
        pass

    @abstractmethod
    async def get_detailed_orders(self, contractor: Contractor, page: int = 1, size: int = 15) -> List[DetailedOrderDTO]:
        """
        Получает список заказов вместе с их сведениями по ID заказчика.

        Заказчик может получить только свои заказы. Параметр `contractor` используется для ограничения доступа заказчика к не принадлежащим ему заказам.

        Args:
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему заказам.
            page (int): Номер страницы.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[DetailedOrderDTO]: Список DTO с подробными данными заказов заказчика.
        """
        pass