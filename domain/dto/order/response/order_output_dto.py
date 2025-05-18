from datetime import datetime, timedelta
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

    @property
    def start_date(self):
        return datetime.combine(self.date, self.start_at)

    @property
    def end_date(self):
        dt = self.date

        if self.start_at > self.end_at:
            dt += timedelta(days=1)

        return datetime.combine(dt, self.end_at)


class OrderWithDetailsOutputDTO(ApplicationDTO):
    order: OrderOutputDTO
    details: List[OrderDetailOutputDTO]


class CompleteOrderOutputDTO(OrderWithDetailsOutputDTO):
    contractor: ContractorOutputDTO
    admin: Optional[AdminOutputDTO]
