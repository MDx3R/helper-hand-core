from typing import List
from abc import ABC, abstractmethod

from domain.dto.order.internal.order_query_dto import (
    GetOrderAfterDTO,
    GetOrderDTO,
)
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderDetailOutputDTO,
)


class ContracteeOrderQueryService(ABC):
    """
    Интерфейс для сервисов заказов исполнителя.

    Этот класс определяет интерфейс для сервисов, отвечающих за возможности исполнителя по работе с заказами.
    """

    @abstractmethod
    async def get_order(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        """
        Получает заказ по его ID.

        Исполнителю доступны только следующие заказы:
        - все открытые заказы
        - все заказы, на которые он отправил отклик.

        Args:
            order_id (int): ID заказа.

        Returns:
            DetailedOrderDTO: DTO с данными заказа.

        Raises:
            RepositoryException: Возникает при ошибках в работе репозиториев.
            ServiceException: Возникает при любых других непредвиденных ошибках в процессе получения заказа.
        """
        pass

    @abstractmethod
    async def get_suitable_order(
        self, query: GetOrderAfterDTO
    ) -> CompleteOrderOutputDTO | None:
        """
        Получает открытый заказ.

        Если `last_order_id` равен `None`, возвращается первый открытый заказ. Иначе, первый открытый заказ после `last_order_id`.

        Args:
            contractee (Contractee): Объект исполнителя.
            last_order_id (int): ID последнего запрошенного заказа.

        Returns:
            DetailedOrderDTO: DTO с данными открытого заказа.

        Raises:
            Exception: Если произошла ошибка при получении открытого заказа.
        """
        pass

    @abstractmethod
    async def get_suitable_details(
        self, query: GetOrderDTO
    ) -> List[OrderDetailOutputDTO]:
        """
        Получает доступные позиции для исполнителя по ID заказа и объекту исполнителя.

        Args:
            order_id (int): ID заказа.
            contractee (Contractee): Объект исполнителя.

        Returns:
            List[OrderDetailDTO]: Список DTO с данными доступных позиций.

        Raises:
            Exception: Если произошла ошибка при получении доступных позиций.
        """
        pass
