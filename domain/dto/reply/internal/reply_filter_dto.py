import datetime
from typing import Optional
from domain.dto.base import InternalDTO, PaginationDTO
from domain.entities.reply.enums import ReplyStatusEnum


class BaseReplyFilterDTO(InternalDTO):
    order_id: Optional[int] = None
    detail_id: Optional[int] = None
    status: Optional[ReplyStatusEnum] = None
    date: Optional[datetime.date] = None


class ContracteeReplyFilterDTO(BaseReplyFilterDTO):
    contractee_id: int


class ReplyFilterDTO(ContracteeReplyFilterDTO, PaginationDTO):
    pass


class CountRepliesDTO(ReplyFilterDTO):
    pass


class RepliedContracteesFilterDTO(BaseReplyFilterDTO, PaginationDTO):
    pass
