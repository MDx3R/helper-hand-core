from domain.dto.base import ApplicationDTO
from domain.entities.order.detail import OrderDetail
from domain.entities.order.order import Order
from domain.entities.user.contractee import Contractee

from .reply import Reply


class CompleteReply(ApplicationDTO):
    """
    Композитная модель отклика на заказ.
    """

    reply: Reply
    contractee: Contractee
    detail: OrderDetail
    order: Order

    @classmethod
    def from_order_detail_contractee(
        cls,
        reply: Reply,
        contractee: Contractee,
        detail: OrderDetail,
        order: Order,
    ) -> "CompleteReply":
        """
        Преобразует `Reply`, `Contractee`, `OrderDetail` и `Order` в `CompleteReply`.
        """
        return cls(
            reply=reply,
            contractee=contractee,
            detail=detail,
            order=order,
        )
