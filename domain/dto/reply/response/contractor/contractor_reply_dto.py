from typing import Optional
from domain.dto.base import ApplicationDTO
from domain.dto.order.response.contractor.contractor_order_output_dto import (
    ContractorViewOrderDetailDTO,
)
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
)


class ContractorViewReplyDTO(ReplyOutputDTO):
    wager: int


class ContractorViewReplyWithContracteeAndDetailDTO(ApplicationDTO):
    reply: ContractorViewReplyDTO
    contractee: ContracteeOutputDTO  # TODO: Поменять на ContractorViewContracteeOutputDTO
    detail: ContractorViewOrderDetailDTO
