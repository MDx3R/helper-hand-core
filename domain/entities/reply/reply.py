from datetime import datetime
from typing import Optional

from domain.entities.base import ApplicationModel

from .enums import ReplyStatusEnum


class Reply(ApplicationModel):
    """
    Связывающая модель сведений о заказе и исполнителя.

    Представляет информацию о конкретном исполнителе, назначенном на определенную позицию в заказе.
    """

    reply_id: Optional[int] = None
    contractee_id: int
    detail_id: int
    wager: int
    status: ReplyStatusEnum = ReplyStatusEnum.created
    dropped: bool = False
    """Флаг, определяющий, был ли отклик отменен системой."""

    paid: Optional[datetime] = None
    """Дата и время произведения оплаты. Может быть `None`, если оплата еще не произведена."""
