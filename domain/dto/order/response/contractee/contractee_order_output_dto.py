from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class ContracteeViewOrderDTO(OrderOutputDTO):
    pass


class ContracteeViewOrderDetailDTO(OrderDetailOutputDTO):
    pass


class ContracteeViewOrderWithDetailsDTO(ApplicationDTO):
    order: ContracteeViewOrderDTO
    details: List[ContracteeViewOrderDetailDTO]
