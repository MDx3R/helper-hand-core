from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.request.order_input_dto import OrderDetailInputDTO, OrderInputDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO


class CreateOrderDTO(ApplicationDTO):
    order: OrderInputDTO
    details: List[OrderDetailInputDTO]
    context: UserContextDTO
