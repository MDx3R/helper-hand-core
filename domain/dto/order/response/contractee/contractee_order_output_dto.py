from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class ContracteeOrderOutputDTO(OrderOutputDTO):
    pass


class ContracteeOrderDetailOutputDTO(OrderDetailOutputDTO):
    pass


class ContracteeOrderWithDetailsOutputDTO(ApplicationDTO):
    order: ContracteeOrderOutputDTO
    details: List[ContracteeOrderDetailOutputDTO]
