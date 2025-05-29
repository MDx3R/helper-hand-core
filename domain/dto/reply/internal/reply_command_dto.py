import datetime
from typing import Optional
from domain.dto.base import InternalDTO
from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.entities.reply.enums import ReplyStatusEnum


class SetReplyStatusDTO(ReplyIdDTO):
    status: ReplyStatusEnum


class DropReplyDTO(InternalDTO):
    contractee_id: Optional[int] = None
    order_id: Optional[int] = None
    detail_id: Optional[int] = None
    date: Optional[datetime.date] = None
    status: Optional[ReplyStatusEnum] = None
