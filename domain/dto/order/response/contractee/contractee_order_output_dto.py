from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class ContracteeViewOrderOutputDTO(OrderOutputDTO):
    pass


class ContracteeViewOrderDetailOutputDTO(OrderDetailOutputDTO):
    pass


class ContracteeViewOrderWithDetailsOutputDTO(ApplicationDTO):
    order: ContracteeViewOrderOutputDTO
    details: List[ContracteeViewOrderDetailOutputDTO]
