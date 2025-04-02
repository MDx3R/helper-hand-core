from typing import List, Optional

from domain.entities.enums import OrderStatusEnum
from domain.dto.input import OrderInputDTO, OrderDetailInputDTO

from .base import (
    ContextDTO,
    OrderIdDTO,
    UserIdDTO,
    PaginationDTO
)

class CreateOrderDTO(ContextDTO):
    order_input: OrderInputDTO
    details_input: List[OrderDetailInputDTO]

class OrderManagementDTO(OrderIdDTO, ContextDTO):
    pass

class GetUserOrdersDTO(UserIdDTO, PaginationDTO):
    pass

class GetUserOrdersWithStatusDTO(GetUserOrdersDTO):
    status: Optional[OrderStatusEnum] = None