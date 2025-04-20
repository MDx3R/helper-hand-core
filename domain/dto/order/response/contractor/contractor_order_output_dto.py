from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class ContractorViewOrderDTO(OrderOutputDTO):
    pass


class ContractorViewOrderDetailDTO(OrderDetailOutputDTO):
    fee: int


class ContractorViewOrderWithDetailsDTO(ApplicationDTO):
    order: ContractorViewOrderDTO
    details: List[ContractorViewOrderDetailDTO]
