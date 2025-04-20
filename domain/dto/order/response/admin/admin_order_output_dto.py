from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class AdminViewOrderOutputDTO(OrderOutputDTO):
    pass


class AdminViewOrderDetailOutputDTO(OrderDetailOutputDTO):
    fee: int


class OrderWithDetailsOutputDTO(ApplicationDTO):
    order: AdminViewOrderOutputDTO
    details: List[AdminViewOrderDetailOutputDTO]
