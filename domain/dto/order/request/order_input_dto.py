from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.base import OrderBaseDTO, OrderDetailBaseDTO


class OrderInputDTO(OrderBaseDTO):
    pass


class OrderDetailInputDTO(OrderDetailBaseDTO):
    pass


class OrderWithDetailsInputDTO(ApplicationDTO):
    order: OrderInputDTO
    details: List[OrderDetailInputDTO]
