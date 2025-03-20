from typing import Optional
from pydantic import BaseModel

from datetime import date, time

from domain.entities import OrderDetail 
from domain.entities.enums import PositionEnum, GenderEnum

class OrderDetailOutputDTO(BaseModel):
    """
    DTO входных данных сведений о заказе.

    Этот класс используется для представления сведений о заказе на уровень представления.
    """

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
    def from_order_detail(cls, detail: OrderDetail) -> 'OrderDetailOutputDTO':
        """
        Преобразует `OrderDetail` в `OrderDetailOutputDTO`.
        """
        return cls(
            detail_id=detail.detail_id,
            order_id=detail.order_id,
            date=detail.date,
            start_at=detail.start_at,
            end_at=detail.end_at,
            position=detail.position,
            gender=detail.gender,
            count=detail.count,
            wager=detail.wager
        )