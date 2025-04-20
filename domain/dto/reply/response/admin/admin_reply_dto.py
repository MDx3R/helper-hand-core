from datetime import datetime
from typing import Optional
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.contractor.contractor_order_output_dto import (
    ContractorViewOrderDetailDTO,
)
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContracteeOutputDTO,
)


class AdminViewReplyDTO(ReplyOutputDTO):
    wager: Optional[int]
    paid: Optional[datetime]


class AdminViewReplyWithContracteeAndDetailDTO(ApplicationDTO):
    reply: AdminViewReplyDTO
    contractee: ContracteeOutputDTO  # TODO: Поменять на AdminViewContracteeOutputDTO
    detail: ContractorViewOrderDetailDTO
