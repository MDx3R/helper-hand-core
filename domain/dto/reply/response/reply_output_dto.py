from domain.dto.base import ApplicationDTO
from domain.dto.order.response.order_output_dto import (
    OrderDetailOutputDTO,
    OrderOutputDTO,
)
from domain.dto.reply.base import ReplyBaseDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
)
from domain.entities.reply.enums import ReplyStatusEnum


class ReplyOutputDTO(ReplyBaseDTO):
    reply_id: int
    status: ReplyStatusEnum
    wager: int
    dropped: bool


class CompleteReplyOutputDTO(ApplicationDTO):
    reply: ReplyOutputDTO
    contractee: ContracteeOutputDTO
    detail: OrderDetailOutputDTO
    order: OrderOutputDTO
