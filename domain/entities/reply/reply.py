from datetime import datetime
from typing import Optional

from domain.entities.base import ApplicationModel

from .enums import ReplyStatusEnum


class Reply(ApplicationModel):
    """
    Связывающая модель сведений о заказе и исполнителя.

    Представляет информацию о конкретном исполнителе, назначенном на определенную позицию в заказе.
    """

    contractee_id: int
    detail_id: int
    wager: int
    status: ReplyStatusEnum = ReplyStatusEnum.created
    paid: Optional[datetime] = None
    """Дата и время произведения оплаты. Может быть `None`, если оплата еще не произведена."""
