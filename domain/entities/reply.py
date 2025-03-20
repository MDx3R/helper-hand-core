from typing import Optional
from .base import ApplicationModel

from datetime import datetime

from .enums import ReplyStatusEnum

class Reply(ApplicationModel):
    """
    Связывающая модель сведений о заказе и исполнителя.

    Представляет информацию о конкретном исполнителе, назначенном на определенную позицию в заказе,
    включая ставку для исполнителя, статус заявки и дату оплаты в случае ее произведения.
    """

    contractee_id: int
    """Идентификатор исполнителя."""

    detail_id: int
    """Идентификатор сведений о заказе."""

    wager: int
    """Ставка для исполнителя."""

    status: ReplyStatusEnum = ReplyStatusEnum.created
    """Статус заявки."""
    
    paid: Optional[datetime] = None
    """Дата и время произведения оплаты. Может быть `None`, если оплата еще не произведена."""