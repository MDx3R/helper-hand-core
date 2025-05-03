from abc import ABC, abstractmethod

from domain.dto.base import LastObjectDTO
from domain.dto.order.internal.order_managment_dto import (
    ApproveOrderDTO,
    CancelOrderDTO,
    CloseOrderDTO,
    FulfillOrderDTO,
    OpenOrderDTO,
    SetOrderActiveDTO,
    TakeOrderDTO,
)
from domain.dto.order.internal.order_query_dto import GetOrderDTO
from domain.dto.order.request.create_order_dto import CreateOrderDTO
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)


class AdminOrderManagementService(ABC):
    @abstractmethod
    async def create_order(
        self, request: CreateOrderDTO
    ) -> OrderWithDetailsOutputDTO:
        """
        Создает заказ от имени администратора.
        Администратор должен иметь профиль заказчика.
        Назначает куратора и публикует заказ сразу.

        Raises:
            PermissionDeniedException: Администратор не имеет профиля заказчика.
        """
        pass

    @abstractmethod
    async def take_order(self, request: TakeOrderDTO) -> OrderOutputDTO:
        """
        Назначает администратора куратором заказа.
        Только для статуса `created` без куратора.

        Raises:
            NotFoundException
            OrderActionNotAllowedException: Куратор уже назначен.
        """
        pass

    @abstractmethod
    async def approve_order(self, request: ApproveOrderDTO) -> OrderOutputDTO:
        """
        Подтверждает заказ.
        Назначает куратора, если его нет.

        Raises:
            NotFoundException
            UnauthorizedAccessException
            OrderStatusChangeNotAllowedException
        """
        pass

    @abstractmethod
    async def cancel_order(self, request: CancelOrderDTO) -> OrderOutputDTO:
        """
        Отменяет заказ (статус `cancelled`).
        Доступно без куратора или только куратору.

        Raises:
            NotFoundException
            UnauthorizedAccessException
            OrderStatusChangeNotAllowedException
        """
        pass

    @abstractmethod
    async def close_order(self, request: CloseOrderDTO) -> OrderOutputDTO:
        """
        Закрывает заказ (статус `closed`).
        Доступно только для куратора.

        Raises:
            NotFoundException
            UnauthorizedAccessException
            OrderStatusChangeNotAllowedException
        """
        pass

    @abstractmethod
    async def open_order(self, request: OpenOrderDTO) -> OrderOutputDTO:
        """
        Открывает заказ (статус `open`).
        Доступно только для куратора.

        Raises:
            NotFoundException
            UnauthorizedAccessException
            OrderStatusChangeNotAllowedException
        """
        pass

    @abstractmethod
    async def set_order_active(
        self, request: SetOrderActiveDTO
    ) -> OrderOutputDTO:
        pass

    @abstractmethod
    async def fulfill_order(self, request: FulfillOrderDTO) -> OrderOutputDTO:
        """
        Завершает заказ.
        Доступно только для куратора.

        Raises:
            NotFoundException
            UnauthorizedAccessException
            OrderStatusChangeNotAllowedException
        """
        pass


class AdminOrderQueryService(ABC):
    @abstractmethod
    async def get_order(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        pass

    @abstractmethod
    async def get_unassigned_order(
        self, query: LastObjectDTO
    ) -> CompleteOrderOutputDTO | None:
        pass
