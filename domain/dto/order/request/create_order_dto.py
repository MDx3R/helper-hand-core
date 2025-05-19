from domain.dto.order.request.order_input_dto import (
    OrderWithDetailsInputDTO,
)
from domain.dto.user.internal.user_context_dto import UserContextDTO


class CreateOrderDTO(OrderWithDetailsInputDTO):
    context: UserContextDTO
