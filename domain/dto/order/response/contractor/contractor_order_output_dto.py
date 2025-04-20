from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class ContractorViewOrderOutputDTO(OrderOutputDTO):
    pass


class ContractorViewOrderDetailOutputDTO(OrderDetailOutputDTO):
    fee: int


class ContractorViewOrderWithDetailsOutputDTO(ApplicationDTO):
    order: ContractorViewOrderOutputDTO
    details: List[ContractorViewOrderDetailOutputDTO]
