from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class AdminOrderOutputDTO(OrderOutputDTO):
    pass


class AdminOrderDetailOutputDTO(OrderDetailOutputDTO):
    fee: int


class AdminOrderWithDetailsOutputDTO(ApplicationDTO):
    order: AdminOrderOutputDTO
    details: List[AdminOrderDetailOutputDTO]
