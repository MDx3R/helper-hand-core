from typing import Optional
from pydantic import BaseModel

from datetime import date, time

from domain.entities import OrderDetail 
from domain.entities.enums import PositionEnum, GenderEnum
from domain.entities.base import ApplicationModel

class OrderDetailInputDTO(BaseModel):
    date: date
    start_at: time
    end_at: time
    position: PositionEnum
    gender: Optional[GenderEnum] = None
    count: int
    wager: int

    def to_order_detail(self, order_id: int) -> OrderDetail:
        """
        Поле `order_id` должно быть установлено с целью поддержки целостности данных.
        """
        return OrderDetail.model_validate(self.model_dump() | {"order_id": order_id})