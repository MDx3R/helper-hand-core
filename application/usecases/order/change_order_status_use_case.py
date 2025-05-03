from typing import Literal

from application.transactions import transactional
from domain.dto.order.response.order_output_dto import OrderOutputDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.order.internal.order_managment_dto import (
    ApproveOrderDTO,
    CancelOrderDTO,
    CloseOrderDTO,
    DisapproveOrderDTO,
    FulfillOrderDTO,
    OpenOrderDTO,
    OrderManagementDTO,
    SetOrderActiveDTO,
)
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.order.order import Order
from domain.exceptions.service import (
    NotFoundException,
    UnauthorizedAccessException,
)
from domain.exceptions.service.orders import (
    OrderStatusChangeNotAllowedException,
)
from domain.mappers.order_mappers import OrderMapper
from domain.repositories.order.order_command_repository import (
    OrderCommandRepository,
)
from domain.repositories.order.order_query_repository import (
    OrderQueryRepository,
)
from domain.services.domain import OrderDomainService


class BaseApproveOrderUseCase:
    def __init__(
        self,
        query_repository: OrderQueryRepository,
        command_repository: OrderCommandRepository,
    ):
        self.query_repository = query_repository
        self.command_repository = command_repository

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
        return order

    async def _get_order_and_raise_if_not_exists(self, order_id: int) -> Order:
        order = await self.query_repository.get_order(order_id)
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
        return await self.command_repository.update_order(order)


class ApproveOrderUseCase(BaseApproveOrderUseCase):
    async def execute(self, request: ApproveOrderDTO) -> OrderOutputDTO:
        return await self._approve_order(request, OrderStatusEnum.open)


class DisapproveOrderUseCase(BaseApproveOrderUseCase):
    async def execute(self, request: DisapproveOrderDTO) -> OrderOutputDTO:
        return await self._approve_order(request, OrderStatusEnum.disapproved)


class BaseChangeOrderStatusUseCase:
    def __init__(
        self,
        query_repository: OrderQueryRepository,
        command_repository: OrderCommandRepository,
    ):
        self.query_repository = query_repository
        self.command_repository = command_repository

    @transactional
    async def _change_status(
        self, request: OrderManagementDTO, status: OrderStatusEnum
    ) -> OrderOutputDTO:
        order = await self._get_order_and_raise_if_not_exists(request.order_id)
        order = await self._change_order_status(order, request.context, status)
        return OrderMapper.to_output(order)

    async def _get_order_and_raise_if_not_exists(self, order_id: int) -> Order:
        order = await self.query_repository.get_order(order_id)
        if not order:
            raise NotFoundException(order_id)
        return order

    async def _change_order_status(
        self, order: Order, context: UserContextDTO, status: OrderStatusEnum
    ) -> Order:
        self._check_order_status_can_be_changed(order, context, status)

        return await self.command_repository.set_order_status(
            order.order_id, status
        )

    def _check_order_status_can_be_changed(
        self, order: Order, context: UserContextDTO, status: OrderStatusEnum
    ):
        if not OrderDomainService.has_supervisor(order):
            raise UnauthorizedAccessException(
                "Невозможно изменить статус заказа без куратора."
            )

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


class CancelOrderUseCase(BaseChangeOrderStatusUseCase):
    async def execute(self, request: CancelOrderDTO) -> OrderOutputDTO:
        return await self._change_status(request, OrderStatusEnum.cancelled)


class CloseOrderUseCase(BaseChangeOrderStatusUseCase):
    async def execute(self, request: CloseOrderDTO) -> OrderOutputDTO:
        return await self._change_status(request, OrderStatusEnum.closed)


class OpenOrderUseCase(BaseChangeOrderStatusUseCase):
    async def execute(self, request: OpenOrderDTO) -> OrderOutputDTO:
        return await self._change_status(request, OrderStatusEnum.open)


class SetActiveOrderUseCase(BaseChangeOrderStatusUseCase):
    async def execute(self, request: SetOrderActiveDTO) -> OrderOutputDTO:
        return await self._change_status(request, OrderStatusEnum.active)


class FulfillOrderUseCase(BaseChangeOrderStatusUseCase):
    async def execute(self, request: FulfillOrderDTO) -> OrderOutputDTO:
        return await self._change_status(request, OrderStatusEnum.fulfilled)
