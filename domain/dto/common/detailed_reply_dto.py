from domain.entities import DetailedReply 

from .reply_dto import ReplyDTO
from .contractee_dto import ContracteeDTO
from .order_detail_dto import OrderDetailDTO
from .order_dto import OrderDTO

class DetailedReplyDTO(ReplyDTO):
    """
    Расширенный `ReplyDTO` для передачи подробных данных отклика на заказ.
    """

    contractee: ContracteeDTO
    detail: OrderDetailDTO
    order: OrderDTO

    @classmethod
    def from_reply(cls, reply: DetailedReply) -> 'DetailedReplyDTO':
        return cls.from_model(reply)