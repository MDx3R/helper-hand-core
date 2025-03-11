from typing import Optional

from domain.models import DetailedReply 

from .reply_dto import ReplyOutputDTO
from .contractee_dto import ContracteeOutputDTO
from .order_detail_dto import OrderDetailOutputDTO
from .order_dto import OrderOutputDTO

class DetailedReplyOutputDTO(ReplyOutputDTO):
    """
    Расширенный `ReplyOutputDTO` для передачи подробных данных отклика на заказ.

    Этот класс используется для представления подробных данных отклика на уровень представления.
    """

    contractee: Optional[ContracteeOutputDTO]
    detail: OrderDetailOutputDTO
    order: Optional[OrderOutputDTO]

    @classmethod
    def from_reply(cls, reply: DetailedReply) -> 'DetailedReplyOutputDTO':
        """
        Преобразует `DetailedReply` в `DetailedReplyOutputDTO`.
        """
        return cls(
            contractee_id=reply.contractee_id,
            detail_id=reply.detail_id,
            wager=reply.wager,
            status=reply.status,
            paid=reply.paid,
            contractee=ContracteeOutputDTO.from_contractee(reply.contractee) if reply.contractee else None,
            detail=OrderDetailOutputDTO.from_order_detail(reply.detail),
            order=OrderOutputDTO.from_order(reply.order) if reply.contractee else None,
        )