from typing import Optional
from pydantic import BaseModel

from datetime import date, time

from domain.entities import OrderDetail 
from domain.entities.enums import PositionEnum, GenderEnum
from domain.dto.base import ApplicationDTO

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

    @classmethod
    def from_order_detail(cls, detail: OrderDetail) -> 'OrderDetailDTO':
        return cls.from_model(detail)