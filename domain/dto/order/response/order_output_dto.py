from typing import List, Optional
from domain.dto.base import ApplicationDTO
from domain.dto.order.base import OrderBaseDTO, OrderDetailBaseDTO
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
