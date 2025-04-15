from datetime import date, datetime, time, timedelta
from typing import Optional

from .base import ApplicationModel
from .enums import GenderEnum, PositionEnum


class OrderDetail(ApplicationModel):
    """
    Модель сведений о заказе. Определяет позицию и дополнительные сведения к ней.

    Представляет информацию о конкретной позиции в заказе, включая дату, время начала и окончания,
    требуемую позицию, количество сотрудников, пол (если требуется) и ставку.
    """

    detail_id: Optional[int] = None
    """Уникальный идентификатор сведений о заказе. Может быть `None` при создании новой записи."""

    order_id: int
    """Идентификатор заказа, к которому относится эти сведения."""

    date: date
    """Дата проведения заказа."""

    start_at: time
    """Время начала работы."""

    end_at: time
    """Время окончания работы."""

    position: PositionEnum
    """Требуемая позиция."""

    count: int
    """Требуемое количество сотрудников на данную позицию."""

    wager: int
    """Полная часовая ставка на данную позицию."""

    fee: int
    """Комиссия сервиса на позицию."""

    gender: Optional[GenderEnum] = None
    """Требуемый пол сотрудников."""

    @property
    def start_date(self):
        return datetime.combine(self.date, self.start_at)

    @property
    def end_date(self):
        dt = self.date

        if self.start_at > self.end_at:
            dt += timedelta(days=1)

        return datetime.combine(dt, self.end_at)
