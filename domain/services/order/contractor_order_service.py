from abc import ABC, abstractmethod

from domain.dto.order.internal.order_managment_dto import (
    CancelOrderDTO,
    SetOrderActiveDTO,
)
from domain.dto.order.internal.order_query_dto import GetOrderDTO
from domain.dto.order.request.create_order_dto import CreateOrderDTO
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)


class ContractorOrderManagementService(ABC):
    @abstractmethod
    async def create_order(
        self, request: CreateOrderDTO
    ) -> OrderWithDetailsOutputDTO:
        """
        Создает новый заказ.

        Основные аспекты:
        - Создание заказа требует подтверждения администратора.
        - Сведения о заказе (`details_input`) обязательны и не могут отсутствовать.
        - После успешного создание заказа отправляется уведомление администраторам.
        """
        pass

    @abstractmethod
    async def cancel_order(self, request: CancelOrderDTO) -> OrderOutputDTO:
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
    async def set_order_active(
        self, request: SetOrderActiveDTO
    ) -> OrderOutputDTO:
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


class ContractorOrderQueryService(ABC):
    @abstractmethod
    async def get_order(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
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
