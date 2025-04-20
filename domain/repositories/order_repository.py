from abc import ABC, abstractmethod
from typing import List

from domain.entities.order.enums import OrderStatusEnum
from domain.entities.order.order import Order
from domain.entities.order.order_with_details import (
    CompleteOrder,
    OrderWithDetails,
    OrderWithDetailsAndContractor,
    OrderWithDetailsAndSupervisor,
)
from domain.entities.user.admin import Admin
from domain.entities.user.contractor import Contractor


class OrderQueryRepository(ABC):
    @abstractmethod
    async def get_order(self, order_id: int) -> Order | None:
        pass

    @abstractmethod
    async def get_order_by_detail_id(self, detail_id: int) -> Order | None:
        pass

    @abstractmethod
    async def get_order_by_id_and_contractor_id(
        self, order_id: int, contractor_id: int
    ) -> Order | None:
        pass

    @abstractmethod
    async def filter_orders(self, page: int = 1, size: int = None) -> List[Order]:
        pass


class CompositeOrderQueryRepository(ABC):
    @abstractmethod
    async def get_order_with_details(self, order_id: int) -> OrderWithDetails | None:
        pass

    @abstractmethod
    async def get_complete_order(self, order_id: int) -> CompleteOrder | None:
        pass

    @abstractmethod
    async def filter_orders_with_details(
        self, page: int = 1, size: int = None
    ) -> List[OrderWithDetails]:
        pass

    @abstractmethod
    async def filter_complete_orders(
        self, page: int = 1, size: int = None
    ) -> List[CompleteOrder]:
        pass

    @abstractmethod
    async def get_unassigned_orders_after(
        self, last_order_id: int = None, size: int = None
    ) -> List[OrderWithDetailsAndContractor]:
        pass


class ContractorOrderQueryRepository(ABC):
    @abstractmethod
    async def get_contractor_by_order_id(self, order_id: int) -> Contractor | None:
        pass

    @abstractmethod
    async def filter_contractor_orders(
        self, contractor_id: int, page: int = 1, size: int = None
    ) -> List[Order]:
        pass

    @abstractmethod
    async def filter_contractor_detailed_orders(
        self, contractor_id: int, page: int = 1, size: int = None
    ) -> List[OrderWithDetailsAndSupervisor]:
        pass


class AdminOrderQueryRepository(ABC):
    @abstractmethod
    async def get_admin_by_order_id(self, order_id: int) -> Admin | None:
        pass

    @abstractmethod
    async def filter_admin_orders(
        self, admin_id: int, page: int = 1, size: int = None
    ) -> List[Order]:
        pass

    @abstractmethod
    async def filter_admin_detailed_orders(
        self, admin_id: int, page: int = 1, size: int = None
    ) -> List[OrderWithDetailsAndContractor]:
        pass


class ContracteeOrderQueryRepository(ABC):
    @abstractmethod
    async def filter_contractee_orders(
        self, contractee_id: int, page: int = 1, size: int = None
    ) -> List[Order]:
        pass

    @abstractmethod
    async def filter_contractee_orders_with_details(
        self, contractee_id: int, page: int = 1, size: int = None
    ) -> List[OrderWithDetails]:
        pass

    @abstractmethod
    async def filter_contractee_complete_orders(
        self, contractee_id: int, page: int = 1, size: int = None
    ) -> List[CompleteOrder]:
        pass


class OrderCommandRepository(ABC):
    @abstractmethod
    async def create_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def update_order(self, order: Order) -> Order:
        pass

    @abstractmethod
    async def set_order_status(self, order_id: int, status: OrderStatusEnum) -> Order:
        pass

    @abstractmethod
    async def set_order_admin(self, order_id: int, admin_id: int) -> Order:
        pass
