from abc import ABC, abstractmethod
from typing import List

from domain.dto.order.internal.base import (
    DetailIdDTO,
    OrderIdDTO,
    OrderSignatureDTO,
)
from domain.dto.order.internal.order_filter_dto import (
    ContracteeOrderFilterDTO,
    OrderFilterDTO,
)
from domain.dto.order.internal.user_command_dto import (
    SetOrderAdminDTO,
    SetOrderStatusDTO,
)
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
    async def get_order(self, query: OrderIdDTO) -> Order | None:
        pass

    @abstractmethod
    async def get_order_by_detail_id(self, query: DetailIdDTO) -> Order | None:
        pass

    @abstractmethod
    async def get_order_by_id_and_contractor_id(
        self, query: OrderSignatureDTO
    ) -> Order | None:
        pass

    @abstractmethod
    async def filter_orders(self, query: OrderFilterDTO) -> List[Order]:
        pass


class CompositeOrderQueryRepository(ABC):
    @abstractmethod
    async def get_order_with_details(
        self, query: OrderIdDTO
    ) -> OrderWithDetails | None:
        pass

    @abstractmethod
    async def get_order_with_details_and_contractor(
        self, query: OrderIdDTO
    ) -> OrderWithDetailsAndContractor | None:
        pass

    @abstractmethod
    async def get_order_with_details_and_supervisor(
        self, query: OrderIdDTO
    ) -> OrderWithDetailsAndSupervisor | None:
        pass

    @abstractmethod
    async def get_complete_order(
        self, query: OrderIdDTO
    ) -> CompleteOrder | None:
        pass

    @abstractmethod
    async def filter_orders_with_details(
        self, query: OrderFilterDTO
    ) -> List[OrderWithDetails]:
        pass

    @abstractmethod
    async def filter_orders_with_details_and_contractor(
        self, query: OrderFilterDTO
    ) -> List[OrderWithDetailsAndContractor]:
        pass

    @abstractmethod
    async def filter_orders_with_details_and_supervisor(
        self, query: OrderFilterDTO
    ) -> List[OrderWithDetailsAndSupervisor]:
        pass

    @abstractmethod
    async def filter_complete_orders(
        self, query: OrderFilterDTO
    ) -> List[CompleteOrder]:
        pass


class ContractorOrderQueryRepository(ABC):
    @abstractmethod
    async def get_contractor_by_order_id(
        self, query: OrderIdDTO
    ) -> Contractor | None:
        pass


class AdminOrderQueryRepository(ABC):
    @abstractmethod
    async def get_admin_by_order_id(self, query: OrderIdDTO) -> Admin | None:
        pass


class ContracteeOrderQueryRepository(ABC):
    @abstractmethod
    async def filter_contractee_orders(
        self, query: ContracteeOrderFilterDTO
    ) -> List[Order]:
        pass

    @abstractmethod
    async def filter_contractee_orders_with_details(
        self, query: ContracteeOrderFilterDTO
    ) -> List[OrderWithDetails]:
        pass

    @abstractmethod
    async def filter_contractee_complete_orders(
        self, query: ContracteeOrderFilterDTO
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
    async def set_order_status(self, query: SetOrderStatusDTO) -> Order:
        pass

    @abstractmethod
    async def set_order_admin(self, query: SetOrderAdminDTO) -> Order:
        pass
