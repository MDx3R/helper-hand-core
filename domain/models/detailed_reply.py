from typing import Optional

from .contractee import Contractee
from .order import Order
from .order_detail import OrderDetail
from .reply import Reply

class DetailedReply(Reply):
    """
    Расширенная модель отклика на заказ.

    Представляет полную информацию о исполнителе, создавшем отклик, выбранной позиции и заказе,
    включая унаследованные поля: ставку для исполнителя, статус заявки и дату оплаты в случае ее произведения.
    
    Объект заказа является необязательным свойством.
    """

    contractee: Optional[Contractee]
    """Объект исполнителя. Может быть `None`."""

    detail: OrderDetail
    """Объект сведений о заказе."""

    order: Optional[Order]
    """Объект заказа. Может быть `None`."""

    @classmethod
    def from_order_detail_contractee(cls, reply: Reply, contractee: Optional[Contractee], detail: OrderDetail, order: Optional[Order]) -> 'Reply':
        """
        Преобразует `Reply`, `Contractee`, `OrderDetail` и `Order` в `Reply`.
        """
        return cls(
            detail_id=reply.detail_id,
            contractee_id=reply.contractee_id,
            wager=reply.wager,
            status=reply.status,
            paid=reply.paid,
            contractee=contractee,
            detail=detail,
            order=order
        )