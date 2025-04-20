from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class OrderOutputForContracteeDTO(OrderOutputDTO):
    pass


class OrderDetailOutputForContracteeDTO(OrderDetailOutputDTO):
    pass


class OrderWithDetailsOutputForContracteeDTO(ApplicationDTO):
    order: OrderOutputForContracteeDTO
    details: List[OrderDetailOutputForContracteeDTO]
