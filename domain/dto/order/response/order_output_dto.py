from typing import List, Optional
from domain.dto.base import ApplicationDTO
from domain.dto.order.base import OrderBaseDTO, OrderDetailBaseDTO
from domain.dto.user.response.admin.admin_output_dto import AdminOutputDTO
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
)
from domain.entities.order.enums import OrderStatusEnum


class OrderOutputDTO(OrderBaseDTO):
    order_id: int
    contractor_id: int
    status: OrderStatusEnum
    admin_id: Optional[int]


class OrderDetailOutputDTO(OrderDetailBaseDTO):
    detail_id: int
    order_id: int


class OrderWithDetailsOutputDTO(ApplicationDTO):
    order: OrderOutputDTO
    details: List[OrderDetailOutputDTO]


class CompleteOrderOutputDTO(ApplicationDTO):
    order: OrderOutputDTO
    details: List[OrderDetailOutputDTO]
    contractor: ContractorOutputDTO
    admin: Optional[AdminOutputDTO]
