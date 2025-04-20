from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class AdminViewOrderDTO(OrderOutputDTO):
    pass


class AdminViewOrderDetailDTO(OrderDetailOutputDTO):
    fee: int


class AdminViewOrderWithDetailsDTO(ApplicationDTO):
    order: AdminViewOrderDTO
    details: List[AdminViewOrderDetailDTO]
