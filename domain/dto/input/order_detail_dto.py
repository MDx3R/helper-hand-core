from datetime import date, time
from typing import Optional

from pydantic import BaseModel

from domain.entities import OrderDetail
from domain.entities.base import ApplicationModel
from domain.entities.enums import GenderEnum, PositionEnum


class OrderDetailInputDTO(BaseModel):
    date: date
    start_at: time
    end_at: time
    position: PositionEnum
    gender: Optional[GenderEnum] = None
    count: int
    wager: int

    def to_order_detail(self, order_id: int, fee: int) -> OrderDetail:
        """
        Поле `order_id` и `fee` должны быть установлены с целью поддержки целостности данных.
        """
        return OrderDetail.model_validate(
            self.model_dump() | {"order_id": order_id, "fee": fee}
        )
