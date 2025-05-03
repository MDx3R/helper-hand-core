from typing import Optional
from domain.dto.order.internal.base import DetailIdDTO, OrderIdDTO
from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.user.internal.base import UserIdDTO
from domain.dto.user.internal.user_context_dto import WithUserContextDTO


class ReplyManagementDTO(ReplyIdDTO, WithUserContextDTO):
    pass


class ApproveReplyDTO(ReplyManagementDTO):
    pass


class DisapproveReplyDTO(ReplyManagementDTO):
    pass


class DropRepliesDTO(WithUserContextDTO):
    order_id: Optional[int] = None
    detail_id: Optional[int] = None
    contractee_id: Optional[int] = None
