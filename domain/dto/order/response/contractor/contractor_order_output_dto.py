from typing import List
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)


class OrderOutputForContractorDTO(OrderOutputDTO):
    pass


class OrderDetailOutputForContractorDTO(OrderDetailOutputDTO):
    fee: int


class OrderWithDetailsOutputForContractorDTO(ApplicationDTO):
    order: OrderOutputForContractorDTO
    details: List[OrderDetailOutputForContractorDTO]
