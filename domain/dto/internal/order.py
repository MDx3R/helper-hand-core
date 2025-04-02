from typing import List, Optional

from domain.entities.enums import OrderStatusEnum
from domain.dto.input import OrderInputDTO, OrderDetailInputDTO

from .base import (
    ContextDTO,
    GetOrderDTO,
    GetUserDTO,
    PaginationDTO
)

class CreateOrderDTO(ContextDTO):
    order_input: OrderInputDTO
    details_input: List[OrderDetailInputDTO]

class OrderManagementDTO(GetOrderDTO, ContextDTO):
    pass

class GetUserOrdersDTO(GetUserDTO, PaginationDTO):
    pass

class GetUserOrdersWithStatusDTO(GetUserOrdersDTO):
    status: Optional[OrderStatusEnum] = None