from abc import ABC, abstractmethod
from typing import List

from domain.dto.common import DetailedOrderDTO, OrderDetailDTO, OrderDTO
from domain.dto.internal import (
    GetOrderDTO,
    GetUserOrderAfterDTO,
    GetUserOrderDTO,
    GetUserOrdersDTO,
    LastObjectDTO,
)
from domain.entities.enums import OrderStatusEnum
from domain.repositories import OrderRepository, ReplyRepository
from domain.services.domain.services import OrderDomainService


# Базовые Use Case для запросов
class GetOrderUseCase(ABC):
    @abstractmethod
    async def get_order(self, query: GetOrderDTO) -> OrderDTO | None:
        pass


class GetDetailedOrderUseCase(ABC):
    @abstractmethod
    async def get_detailed_order(
        self, query: GetOrderDTO
    ) -> DetailedOrderDTO | None:
        pass


class GetOrderUseCaseFacade(GetOrderUseCase, GetDetailedOrderUseCase):
    def __init__(
        self,
        order_repository: OrderRepository,
    ):
        self.order_repository = order_repository

    async def get_order(self, query: GetOrderDTO) -> OrderDTO | None:
        order = await self.order_repository.get_order(query.order_id)
        if not order:
            return None
        return OrderDTO.from_order(order)

    async def get_detailed_order(
        self, query: GetOrderDTO
    ) -> DetailedOrderDTO | None:
        order = await self.order_repository.get_detailed_order(query.order_id)
        if not order:
            return None
        return DetailedOrderDTO.from_order(order)


class GetContractorOrderUseCase(ABC):
    @abstractmethod
    async def get_order(self, query: GetUserOrderDTO) -> OrderDTO | None:
        pass


class GetContractorDetailedOrderUseCase(ABC):
    @abstractmethod
    async def get_detailed_order(
        self, query: GetUserOrderDTO
    ) -> DetailedOrderDTO | None:
        pass


class GetContractorOrderUseCaseFacade(
    GetContractorOrderUseCase, GetContractorDetailedOrderUseCase
):
    def __init__(
        self,
        order_repository: OrderRepository,
    ):
        self.order_repository = order_repository

    async def get_order(self, query: GetUserOrderDTO) -> OrderDTO | None:
        order = await self.order_repository.get_order_by_id_and_contractor_id(
            query.order_id, query.user_id
        )
        if not order:
            return None
        return OrderDTO.from_order(order)

    async def get_detailed_order(
        self, query: GetUserOrderDTO
    ) -> DetailedOrderDTO | None:
        order = await self.order_repository.get_detailed_order_by_id_and_contractor_id(
            query.order_id, query.user_id
        )
        if not order:
            return None
        return DetailedOrderDTO.from_order(order)


# Questionable
# TODO: Revise
class HasContracteeRepliedToOrderUseCase:
    def __init__(
        self,
        reply_repository: ReplyRepository,
    ):
        self.reply_repository = reply_repository

    async def has_contractee_replied(self, query: GetUserOrderDTO) -> bool:
        return await self.reply_repository.has_contractee_replied_to_order(
            query.order_id, query.user_id
        )


# Questionable
# TODO: Revise
class GetAvailableOrInvolvedOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
        get_order_use_case: GetOrderUseCase,
        contractee_reply_use_case: HasContracteeRepliedToOrderUseCase,
    ):
        self.order_repository = order_repository
        self.get_order_use_case = get_order_use_case
        self.contractee_reply_use_case = contractee_reply_use_case

    async def get_order(self, query: GetUserOrderDTO) -> OrderDTO | None:
        order = await self.get_order_use_case.get_order(
            GetOrderDTO(order_id=query.order_id)
        )
        if not order:
            return None

        if OrderDomainService.is_available(order):
            return order
        if self.contractee_reply_use_case.has_contractee_replied(query):
            return order

        return None


class GetContracteeOrdersUseCase(ABC):
    @abstractmethod
    async def get_contractee_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderDTO]:
        pass


class GetContractorOrdersUseCase(ABC):
    @abstractmethod
    async def get_contractor_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderDTO]:
        pass


class GetAdminOrdersUseCase(ABC):
    @abstractmethod
    async def get_admin_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderDTO]:
        pass


class GetUserOrdersUseCaseFacade(
    GetContracteeOrdersUseCase,
    GetContractorOrdersUseCase,
    GetAdminOrdersUseCase,
):
    def __init__(
        self,
        order_repository: OrderRepository,
    ):
        self.order_repository = order_repository

    async def get_contractee_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderDTO]:
        orders = await self.order_repository.get_contractee_orders_by_page(
            query.user_id, query.page, query.size
        )
        return [OrderDTO.from_order(elem) for elem in orders]

    async def get_contractor_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderDTO]:
        orders = await self.order_repository.get_contractor_orders_by_page(
            query.user_id, query.page, query.size
        )
        return [OrderDTO.from_order(elem) for elem in orders]

    async def get_admin_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderDTO]:
        orders = await self.order_repository.get_admin_orders_by_page(
            query.user_id, query.page, query.size
        )
        return [OrderDTO.from_order(elem) for elem in orders]


# Специфичные Use Case
class GetUnassignedOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
    ):
        self.order_repository = order_repository

    async def get_unassigned_order(
        self, query: LastObjectDTO
    ) -> DetailedOrderDTO | None:
        orders = (
            await self.order_repository.get_detailed_unassigned_orders_after(
                query.last_id, size=1
            )
        )
        if not orders:
            return None
        return DetailedOrderDTO.from_order(orders[0])


# Ridiculously Hard
# TODO: Revise
class GetOpenAndSuitableOrderUseCase(ABC):
    @abstractmethod
    async def get_open_order(
        self, query: GetUserOrderAfterDTO
    ) -> DetailedOrderDTO | None:
        pass


# Ridiculously Hard
# TODO: Revise
class GetAvailableDetailsUseCase(ABC):
    @abstractmethod
    async def get_available_details(
        self, query: GetUserOrderDTO
    ) -> List[OrderDetailDTO]:
        pass
