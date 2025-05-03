from application.usecases.order.create_order_use_case import (
    CreateOrderWithDetailsUseCase,
)
from domain.dto.order.request.order_input_dto import OrderInputDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.order.order import Order
from domain.mappers.order_mappers import OrderMapper


class CreateOrderWithDetailsForAdminUseCase(CreateOrderWithDetailsUseCase):
    def _build_order(
        self, order_input: OrderInputDTO, context: UserContextDTO
    ) -> Order:
        order = OrderMapper.from_input(order_input, context.user_id)
        order.status = OrderStatusEnum.open
        order.admin_id = context.user_id
        return order
