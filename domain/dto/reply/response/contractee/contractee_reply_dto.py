from datetime import datetime
from typing import Optional
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.contractee.contractee_order_output_dto import (
    ContracteeViewOrderDTO,
    ContracteeViewOrderDetailDTO,
)
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO


class ContracteeViewReplyDTO(ReplyOutputDTO):
    wager: Optional[int]
    paid: Optional[datetime]


class ContracteeViewReplyWithOrderAndDetailDTO(ApplicationDTO):
    reply: ContracteeViewReplyDTO
    order: ContracteeViewOrderDTO
    detail: ContracteeViewOrderDetailDTO
