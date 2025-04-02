from abc import ABC, abstractmethod
from typing import List

from domain.dto.common import OrderDTO, DetailedOrderDTO

from domain.dto.internal import (
    CreateOrderDTO,
    OrderManagementDTO,
    PaginationDTO,
    GetOrderDTO,
    GetUserOrdersDTO,
    LastObjectDTO
)

class AdminOrderCreationService(ABC):
    @abstractmethod
    async def create_order(
        self,
        request: CreateOrderDTO
    ) -> DetailedOrderDTO:
        """
        Создает заказ от имени администратора. 
        Администратор должен иметь профиль заказчика. 
        Назначает куратора и публикует заказ сразу.

        Raises:
            PermissionDeniedException: Администратор не имеет профиля заказчика.
        """
        pass

class AdminOrderManagementService(ABC):
    @abstractmethod
    async def take_order(self, action: OrderManagementDTO) -> OrderDTO:
        """
        Назначает администратора куратором заказа. 
        Только для статуса `created` без куратора.

        Raises:
            NotFoundException
            OrderActionNotAllowedException: Куратор уже назначен.
        """
        pass

    @abstractmethod
    async def approve_order(self, action: OrderManagementDTO) -> OrderDTO:
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
    async def cancel_order(self, action: OrderManagementDTO) -> OrderDTO:
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
    async def lock_order(self, action: OrderManagementDTO) -> OrderDTO:
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
    async def open_order(self, action: OrderManagementDTO) -> OrderDTO:
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
    async def fulfill_order(self, action: OrderManagementDTO) -> OrderDTO:
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
    async def get_order(self, query: GetOrderDTO) -> OrderDTO | None:
        pass

    @abstractmethod
    async def get_detailed_order(self, query: GetOrderDTO) -> DetailedOrderDTO | None:
        pass

    @abstractmethod
    async def get_unassigned_order(self, query: LastObjectDTO) -> DetailedOrderDTO | None:
        pass

    @abstractmethod
    async def get_orders(self, query: PaginationDTO) -> List[OrderDTO]:
        pass

    @abstractmethod
    async def get_detailed_orders(self, query: PaginationDTO) -> List[DetailedOrderDTO]:
        pass

class AdminRoleAssociatedOrderQueryService(ABC):
    @abstractmethod
    async def get_contractee_orders(self, query: GetUserOrdersDTO) -> List[OrderDTO]:
        pass

    @abstractmethod
    async def get_contractor_orders(self, query: GetUserOrdersDTO) -> List[OrderDTO]:
        pass

    @abstractmethod
    async def get_admin_orders(self, query: GetUserOrdersDTO) -> List[OrderDTO]:
        pass