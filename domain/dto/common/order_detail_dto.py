from datetime import date, time
from typing import Optional

from pydantic import BaseModel

from domain.dto.base import ApplicationDTO
from domain.entities import OrderDetail
from domain.entities.enums import GenderEnum, PositionEnum


class OrderDetailDTO(ApplicationDTO):
    detail_id: int
    order_id: int
    date: date
    start_at: time
    end_at: time
    position: PositionEnum
    gender: Optional[GenderEnum]
    count: int
    wager: int
    fee: int

    @classmethod
    def from_order_detail(cls, detail: OrderDetail) -> "OrderDetailDTO":
        return cls.from_model(detail)

    def to_order_detail(self) -> "OrderDetail":
        return OrderDetail.model_validate(self.model_dump())
