from typing import List

from domain.dto.common import OrderDTO
from domain.dto.input import OrderDetailInputDTO

from .base import InternalDTO


class CreateOrderDetailDTO(InternalDTO):
    order: OrderDTO
    detail: OrderDetailInputDTO


class CreateOrderDetailsDTO(InternalDTO):
    order: OrderDTO
    details: List[OrderDetailInputDTO]
