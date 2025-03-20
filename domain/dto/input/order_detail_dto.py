from typing import Optional
from pydantic import BaseModel

from datetime import date, time

from domain.entities import OrderDetail 
from domain.entities.enums import PositionEnum, GenderEnum

class OrderDetailInputDTO(BaseModel):
    """
    DTO входных данных сведений о заказе.

    Этот класс используется для представления данных сведений о заказе, полученных из внешнего источника. 
    Он предназначен для валидации входных данных перед передачей в бизнес-логику.
    """

    date: date
    start_at: time
    end_at: time
    position: PositionEnum
    gender: Optional[GenderEnum] = None
    count: int
    wager: int

    def to_order_detail(self, order_id: int) -> OrderDetail:
        """
        Преобразует `OrderDetailInputDTO` в `OrderDetail`.
        
        Поле `order_id` должно быть установлено для корректного сохранения модели.
        """
        return OrderDetail(
            order_id=order_id,
            date=self.date,
            start_at=self.start_at,
            end_at=self.end_at,
            position=self.position,
            gender=self.gender,
            count=self.count,
            wager=self.wager
        )