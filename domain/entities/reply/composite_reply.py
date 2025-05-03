from domain.entities.base import ApplicationModel
from domain.entities.order.detail import OrderDetail
from domain.entities.order.order import Order
from domain.entities.user.contractee.contractee import Contractee

from .reply import Reply


class ReplyWithContracteeAndDetail(ApplicationModel):
    """
    Композитная модель отклика на заказ с исполнителем и позицией.
    """

    reply: Reply
    contractee: Contractee
    detail: OrderDetail


class CompleteReply(ApplicationModel):
    """
    Композитная модель отклика на заказ.
    """

    reply: Reply
    contractee: Contractee
    detail: OrderDetail
    order: Order
