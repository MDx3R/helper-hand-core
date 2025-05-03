import datetime
from typing import Optional
from domain.dto.base import InternalDTO, PaginationDTO, SortingDTO
from domain.entities.reply.enums import ReplyStatusEnum


class BaseReplyFilterDTO(InternalDTO):
    order_id: Optional[int] = None
    detail_id: Optional[int] = None
    status: Optional[ReplyStatusEnum] = None
    dropped: Optional[bool] = None
    date: Optional[datetime.date] = None


class ContracteeReplyFilterDTO(BaseReplyFilterDTO):
    contractee_id: Optional[int] = None


class ReplyFilterDTO(ContracteeReplyFilterDTO, PaginationDTO, SortingDTO):
    pass


class CountRepliesDTO(ReplyFilterDTO):
    pass


class RepliedContracteesFilterDTO(BaseReplyFilterDTO, PaginationDTO):
    pass
