from application.transactions import transactional
from domain.dto.order.internal.order_managment_dto import TakeOrderDTO
from domain.dto.order.internal.user_command_dto import SetOrderAdminDTO
from domain.dto.order.response.order_output_dto import OrderOutputDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.entities.order.order import Order
from domain.exceptions.service.common import NotFoundException
from domain.exceptions.service.orders import (
    OrderSupervisorAssignmentNotAllowedException,
)
from domain.mappers.order_mappers import OrderMapper
from domain.repositories.order.order_command_repository import (
    OrderCommandRepository,
)
from domain.repositories.order.order_query_repository import (
    OrderQueryRepository,
)
from domain.services.domain.services import OrderDomainService


class TakeOrderUseCase:
    def __init__(
        self,
        query_repository: OrderQueryRepository,
        command_repository: OrderCommandRepository,
    ):
        self.query_repository = query_repository
        self.command_repository = command_repository

    @transactional
    async def execute(self, request: TakeOrderDTO) -> OrderOutputDTO:
        order = await self._get_order_and_raise_if_not_exists(request.order_id)
        order = await self._take_order(order, request.context)
        return OrderMapper.to_output(order)

    async def _get_order_and_raise_if_not_exists(self, order_id: int) -> Order:
        order = await self.query_repository.get_order(order_id)
        if not order:
            raise NotFoundException(order_id)
        return order

    async def _take_order(
        self, order: Order, context: UserContextDTO
    ) -> Order:
        if not order.order_id:
            raise

        if not OrderDomainService.can_be_assigned(order):
            raise OrderSupervisorAssignmentNotAllowedException(order.order_id)

        return await self.command_repository.set_order_admin(
            SetOrderAdminDTO(order_id=order.order_id, admin_id=context.user_id)
        )
