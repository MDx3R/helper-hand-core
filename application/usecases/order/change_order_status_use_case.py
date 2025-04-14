from abc import ABC, abstractmethod
from typing import Literal

from application.transactions import transactional
from domain.dto.common import OrderDTO
from domain.dto.context import UserContextDTO
from domain.dto.internal import (
    ApproveOrderDTO,
    CancelOrderDTO,
    CloseOrderDTO,
    FulfillOrderDTO,
    OpenOrderDTO,
    SetOrderActiveDTO,
    TakeOrderDTO,
)
from domain.dto.internal.order import DisapproveOrderDTO, OrderManagementDTO
from domain.entities import Order
from domain.entities.enums import OrderStatusEnum
from domain.exceptions.service import (
    NotFoundException,
    OrderSupervisorAssignmentNotAllowedException,
    UnauthorizedAccessException,
)
from domain.exceptions.service.orders import (
    OrderStatusChangeNotAllowedException,
)
from domain.repositories import OrderRepository
from domain.services.domain import OrderDomainService


class TakeOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
    ):
        self.order_repository = order_repository

    @transactional
    async def take_order(self, request: TakeOrderDTO) -> OrderDTO:
        order = await self._get_order_and_raise_if_not_exists(request.order_id)
        order = await self._take_order(order, request.context)
        return OrderDTO.from_order(order)

    async def _get_order_and_raise_if_not_exists(self, order_id: int) -> Order:
        order = await self.order_repository.get_order(order_id)
        if not order:
            raise NotFoundException(order_id)
        return order

    async def _take_order(
        self, order: Order, context: UserContextDTO
    ) -> Order:
        self._check_order_can_be_assigned(order)

        order.admin_id = context.user_id
        return await self.order_repository.save_order(order)

    def _check_order_can_be_assigned(self, order: Order):
        if not OrderDomainService.can_be_assigned(order):
            raise OrderSupervisorAssignmentNotAllowedException(order.order_id)


class ApproveOrderUseCase(ABC):
    @abstractmethod
    async def approve_order(self, request: ApproveOrderDTO) -> OrderDTO:
        pass


class DisapproveOrderUseCase(ABC):
    @abstractmethod
    async def disapprove_order(self, request: DisapproveOrderDTO) -> OrderDTO:
        pass


class ApproveOrderUseCaseFacade(ApproveOrderUseCase, DisapproveOrderUseCase):
    def __init__(
        self,
        order_repository: OrderRepository,
    ):
        self.order_repository = order_repository

    async def approve_order(self, request: ApproveOrderDTO) -> OrderDTO:
        return await self._approve_order(request, OrderStatusEnum.open)

    async def disapprove_order(self, request: DisapproveOrderDTO) -> OrderDTO:
        return await self._approve_order(request, OrderStatusEnum.disapproved)

    @transactional
    async def _approve_order(
        self,
        request: ApproveOrderDTO,
        status: Literal[OrderStatusEnum.disapproved, OrderStatusEnum.open],
    ) -> Order:
        order = await self._get_order_and_raise_if_not_exists(request.order_id)
        self._check_order_can_be_approved(order, request.context, status)

        # Можно установить admin_id явно,
        # так как при вызове use case заказ или не имеет куратора, или имеет такого же
        order.admin_id = request.context.user_id
        order.status = status
        order = await self._save_order(order)
        return OrderDTO.from_order(order)

    async def _get_order_and_raise_if_not_exists(self, order_id: int) -> Order:
        order = await self.order_repository.get_order(order_id)
        if not order:
            raise NotFoundException(order_id)
        return order

    def _check_order_can_be_approved(
        self, order: Order, context: UserContextDTO, status: OrderStatusEnum
    ):
        if OrderDomainService.has_supervisor(
            order
        ) and not OrderDomainService.is_supervised_by(order, context.user_id):
            raise UnauthorizedAccessException(
                "Невозможно изменить статус чужого заказа."
            )

        if not OrderDomainService.can_be_approved(order):
            raise OrderStatusChangeNotAllowedException(
                order.order_id, status=status
            )

    async def _save_order(self, order: Order) -> Order:
        return await self.order_repository.save_order(order)


class CancelOrderUseCase(ABC):
    @abstractmethod
    async def cancel_order(self, request: CancelOrderDTO) -> OrderDTO:
        pass


class CloseOrderUseCase(ABC):
    @abstractmethod
    async def close_order(self, request: CloseOrderDTO) -> OrderDTO:
        pass


class OpenOrderUseCase(ABC):
    @abstractmethod
    async def open_order(self, request: OpenOrderDTO) -> OrderDTO:
        pass


class SetActiveOrderUseCase(ABC):
    @abstractmethod
    async def set_order_active(self, request: SetOrderActiveDTO) -> OrderDTO:
        pass


class FulfillOrderUseCase(ABC):
    @abstractmethod
    async def fulfill_order(self, request: FulfillOrderDTO) -> OrderDTO:
        pass


class ChangeOrderStatusUseCaseFacade(
    CancelOrderUseCase,
    CloseOrderUseCase,
    OpenOrderUseCase,
    SetActiveOrderUseCase,
    FulfillOrderUseCase,
):
    def __init__(
        self,
        order_repository: OrderRepository,
    ):
        self.order_repository = order_repository

    async def cancel_order(self, request: CancelOrderDTO) -> OrderDTO:
        return await self.change_order_status(
            request, OrderStatusEnum.cancelled
        )

    async def close_order(self, request: CloseOrderDTO) -> OrderDTO:
        return await self.change_order_status(request, OrderStatusEnum.closed)

    async def open_order(self, request: OpenOrderDTO) -> OrderDTO:
        return await self.change_order_status(request, OrderStatusEnum.open)

    async def set_order_active(self, request: SetOrderActiveDTO) -> OrderDTO:
        return await self.change_order_status(request, OrderStatusEnum.active)

    async def fulfill_order(self, request: FulfillOrderDTO) -> OrderDTO:
        return await self.change_order_status(
            request, OrderStatusEnum.fulfilled
        )

    @transactional
    async def change_order_status(
        self, request: OrderManagementDTO, status: OrderStatusEnum
    ) -> OrderDTO:
        order = await self._get_order_and_raise_if_not_exists(request.order_id)
        order = await self._change_order_status(order, request.context, status)
        return OrderDTO.from_order(order)

    async def _get_order_and_raise_if_not_exists(self, order_id: int) -> Order:
        order = await self.order_repository.get_order(order_id)
        if not order:
            raise NotFoundException(order_id)
        return order

    async def _change_order_status(
        self, order: Order, context: UserContextDTO, status: OrderStatusEnum
    ) -> Order:
        self._check_order_status_can_be_changed(order, context, status)

        return await self.order_repository.change_order_status(
            order.order_id, status
        )

    def _check_order_status_can_be_changed(
        self, order: Order, context: UserContextDTO, status: OrderStatusEnum
    ):
        if not (
            OrderDomainService.is_supervised_by(order, context.user_id)
            or OrderDomainService.is_owned_by(order, context.user_id)
        ):
            raise UnauthorizedAccessException(
                "Невозможно изменить статус чужого заказа."
            )

        if not OrderDomainService.can_status_be_changed(order, status):
            raise OrderStatusChangeNotAllowedException(
                order.order_id,
                status,
            )
