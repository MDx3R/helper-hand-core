from typing import List
from abc import ABC, abstractmethod

from domain.models import Order, Admin

from application.dtos.input import OrderInputDTO, OrderDetailInputDTO
from application.dtos.output import DetailedOrderOutputDTO, OrderOutputDTO

class AdminOrderService(ABC):
    @abstractmethod
    async def create_order(self, order_input: OrderInputDTO, details_input: List[OrderDetailInputDTO], admin: Admin) -> DetailedOrderOutputDTO:
        """
        Создает новый заказ от имени администратора.

        Основные аспекты:
        - Для создания заказа у администратора должен быть профиль заказчика.
        - Сведения о заказе (`details_input`) обязательны и не могут отсутствовать.
        - Заказ не требует подтверждения, куратором становится администратор, создавший заказ и публикуется сразу.

        Args:
            order_input (OrderInputDTO): DTO с данными для создания заказа.
            details_input (List[OrderDetailInputDTO]): Список DTO с сведениями заказа. Не может быть пустым.
            admin (Admin): Объект администратора.

        Returns:
            DetailedOrderOutputDTO: DTO с данными созданного заказа вместе с его сведениями.

        Raises:
            MissingOrderDetailsException: Возникает, если отсутствуют сведения заказа.
            IntegrityException: Возникает при нарушении целостности данных.
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках в процессе создания заказа.
        """
        pass
    
    @abstractmethod
    async def get_order(self, order_id: int, admin: Admin) -> OrderOutputDTO | None:
        """
        Получает заказ по его ID.

        Администраторам доступны все заказы.

        Args:
            order_id (int): ID заказа.
            admin (Admin): Объект администратора.

        Returns:
            OrderOutputDTO: DTO с данными заказа или `None`, если заказ не найден.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_detailed_order(self, order_id: int, admin: Admin) -> DetailedOrderOutputDTO | None:
        """
        Получает заказ вместе с его сведениями по его ID.

        Администраторам доступны все заказы.

        Args:
            order_id (int): ID заказа.
            admin (Admin): Объект администратора.

        Returns:
            DetailedOrderOutputDTO: DTO с данными созданного заказа вместе с его сведениями или `None`, если заказ не найден.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def take_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        """
        Назначает администратора куратором заказа.

        Назначение куратора возможно только для заказов со статусом `created`.

        Args:
            order_id (int): ID заказа.
            admin (Admin): Объект администратора.

        Returns:
            OrderOutputDTO: DTO с данными заказа.

        Raises:
            NotFoundException: Возникает, если заказ не был найден.
            OrderStatusChangeNotAllowedException: Возникает, если заказ не может быть отменен.
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def approve_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        """
        Подтверждает заказ.

        Подтверждение заказа возможно только для заказов со статусом `created` и не имеющих назначенного куратора.
        Если куратор отсутствует, после подтверждения администратор становится куратором заказа.

        Args:
            order_id (int): ID заказа.
            admin (Admin): Объект администратора.

        Returns:
            OrderOutputDTO: DTO с данными заказа.

        Raises:
            NotFoundException: Возникает, если заказ не был найден.
            OrderStatusChangeNotAllowedException: Возникает, если заказ не может быть отменен.
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def cancel_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        """
        Отменяет заказ по его ID: устанавливается статус сброшен (`cancelled`).

        Основные аспекты отмены заказа:
        - Любой неподтвержденный заказ может быть отменен администратором.
        - Подтвержденный заказ может быть отмен только куратором этого заказа.
        - После подтверждения отмена заказа отправляет уведомление назначенному заказчику и исполнителю соответствующие уведомления. 
        Все отклики отменяются автоматически.
        - Завершенный заказ не может быть отменен.

        Args:
            order_id (int): ID заказа.
            admin (Admin): Объект администратора.

        Returns:
            OrderOutputDTO: DTO с данными заказа.

        Raises:
            NotFoundException: Возникает, если заказ не был найден.
            UnauthorizedAccessException: Возникает, если администратор пытается отменить заказ, который не принадлежит ему.
            OrderStatusChangeNotAllowedException: Возникает, если заказ не может быть отменен.
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def lock_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        """
        Закрывает заказ по его ID: устанавливается статус закрыт (`closed`).

        Закрыть заказ может только куратор. Закрытие заказа возможно, только если он является открытым.

        Args:
            order_id (int): ID заказа.
            admin (Admin): Объект администратора.

        Returns:
            OrderOutputDTO: DTO с данными заказа.

        Raises:
            NotFoundException: Возникает, если заказ не был найден.
            UnauthorizedAccessException: Возникает, если администратор пытается закрыть заказ, который не принадлежит ему.
            OrderStatusChangeNotAllowedException: Возникает, если заказ не может быть отменен.
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def unlock_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        """
        Заново открывает заказ по его ID: устанавливается статус открыт (`open`).

        Открыть заказ может только куратор. Открытие заказа возможно, только если он является закрытым.

        Args:
            order_id (int): ID заказа.
            admin (Admin): Объект администратора.

        Returns:
            OrderOutputDTO: DTO с данными заказа.

        Raises:
            NotFoundException: Возникает, если заказ не был найден.
            UnauthorizedAccessException: Возникает, если администратор пытается закрыть заказ, который не принадлежит ему.
            OrderStatusChangeNotAllowedException: Возникает, если заказ не может быть отменен.
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def fulfill_order(self, order_id: int, admin: Admin) -> OrderOutputDTO:
        """
        Завершает заказ.

        Завершить заказ может только куратор. Завершить можно только активный заказ.

        Args:
            order_id (int): ID заказа.
            admin (Admin): Объект администратора.

        Returns:
            OrderOutputDTO: DTO с данными заказа.

        Raises:
            NotFoundException: Возникает, если заказ не был найден.
            UnauthorizedAccessException: Возникает, если администратор пытается закрыть заказ, который не принадлежит ему.
            OrderStatusChangeNotAllowedException: Возникает, если заказ не может быть отменен.
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[OrderOutputDTO]:
        """
        Получает список заказов в порядке убывания даты.

        Args:
            admin (Admin): Объект администратора.
            page (int): Номер страницы. По умолчанию номер страницы равен 1.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[OrderOutputDTO]: Список DTO с заказами.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_detailed_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[DetailedOrderOutputDTO]:
        """
        Получает список заказов вместе с их сведениями в порядке убывания даты.

        Args:
            admin (Admin): Объект администратора.
            page (int): Номер страницы. По умолчанию номер страницы равен 1.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[DetailedOrderOutputDTO]: Список DTO с подробными данными заказов.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_one_unassigned_order(self, admin: Admin, last_order_id: int = None) -> DetailedOrderOutputDTO | None:
        """
        Получает список открытых заказов с их сведениями.

        Если `last_order_id` равен `None`, возвращается первый открытый заказ. Иначе, первый открытый заказ после `last_order_id`.

        Args:
            admin (Admin): Объект администратора.
            last_order_id (int): ID последнего запрошенного заказа.

        Returns:
            DetailedOrderOutputDTO: DTO с данными заказа вместе с его сведениями.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_open_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[DetailedOrderOutputDTO]:
        """
        Получает список открытых заказов с их сведениями.

        Args:
            admin (Admin): Объект администратора.
            page (int): Номер страницы. По умолчанию номер страницы равен 1.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[DetailedOrderOutputDTO]: Список DTO с данными заказов вместе с их сведениями.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_closed_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[DetailedOrderOutputDTO]:
        """
        Получает список закрытых заказов с их сведениями.

        Args:
            admin (Admin): Объект администратора.
            page (int): Номер страницы. По умолчанию номер страницы равен 1.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[DetailedOrderOutputDTO]: Список DTO с данными заказов вместе с их сведениями.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_active_orders(self, admin: Admin, page: int = 1, size: int = 15) -> List[DetailedOrderOutputDTO]:
        """
        Получает список активных заказов с их сведениями.

        Args:
            admin (Admin): Объект администратора.
            page (int): Номер страницы. По умолчанию номер страницы равен 1.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[DetailedOrderOutputDTO]: Список DTO с данными заказов вместе с их сведениями.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_contractee_orders(self, contractee_id: int, admin: Admin, page: int = 1, size: int = 15) -> List[DetailedOrderOutputDTO]:
        """
        Получает список заказов исполнителя с их сведениями.

        Args:
            contractee_id (int): ID исполнителя.
            admin (Admin): Объект администратора.
            page (int): Номер страницы. По умолчанию номер страницы равен 1.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[DetailedOrderOutputDTO]: Список DTO с данными заказов вместе с их сведениями.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_contractor_orders(self, contractor_id: int, admin: Admin, page: int = 1, size: int = 15) -> List[DetailedOrderOutputDTO]:
        """
        Получает список заказов заказчика с их сведениями.

        Args:
            contractor_id (int): ID заказчика.
            admin (Admin): Объект администратора.
            page (int): Номер страницы. По умолчанию номер страницы равен 1.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[DetailedOrderOutputDTO]: Список DTO с данными заказов вместе с их сведениями.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass

    @abstractmethod
    async def get_admin_orders(self, admin_id: int, admin: Admin, page: int = 1, size: int = 15) -> List[DetailedOrderOutputDTO]:
        """
        Получает список заказов, курируемых администратором, вместе со сведениями заказов.

        Args:
            admin_id (int): ID запрашиваемого администратора.
            admin (Admin): Объект администратора, запрашивающего список заказов.
            page (int): Номер страницы. По умолчанию номер страницы равен 1.
            size (int): Размер страницы. По умолчанию размер страницы равен 15.

        Returns:
            List[DetailedOrderOutputDTO]: Список DTO с данными заказов вместе с их сведениями.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках.
        """
        pass