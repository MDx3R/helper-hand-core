from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class ContractorOrderOutputDTO(OrderOutputDTO):
    pass


class ContractorOrderDetailOutputDTO(OrderDetailOutputDTO):
    fee: int


class ContractorOrderWithDetailsOutputDTO(ApplicationDTO):
    order: ContractorOrderOutputDTO
    details: List[ContractorOrderDetailOutputDTO]
