from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class OrderOutputForAdminDTO(OrderOutputDTO):
    pass


class OrderDetailOutputForAdminDTO(OrderDetailOutputDTO):
    fee: int


class OrderWithDetailsOutputForAdminDTO(ApplicationDTO):
    order: OrderOutputForAdminDTO
    details: List[OrderDetailOutputForAdminDTO]
