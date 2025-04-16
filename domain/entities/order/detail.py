from datetime import date, datetime, time, timedelta
from typing import Optional

from domain.entities.base import ApplicationModel
from domain.entities.enums import GenderEnum, PositionEnum


class OrderDetail(ApplicationModel):
    """
    Модель сведений о заказе. Определяет позицию и дополнительные сведения к ней.

    Представляет информацию о конкретной позиции в заказе.
    """

    detail_id: Optional[int] = None
    """Уникальный идентификатор сведений о заказе. Может быть `None` при создании новой записи."""

    order_id: int
    date: date
    start_at: time
    end_at: time
    position: PositionEnum
    count: int
    wager: int
    fee: int
    gender: Optional[GenderEnum] = None

    @property
    def start_date(self):
        return datetime.combine(self.date, self.start_at)

    @property
    def end_date(self):
        dt = self.date

        if self.start_at > self.end_at:
            dt += timedelta(days=1)

        return datetime.combine(dt, self.end_at)
