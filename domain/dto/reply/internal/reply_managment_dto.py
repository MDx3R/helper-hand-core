from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO


class ReplyManagementDTO(ReplyIdDTO):
    context: UserContextDTO


class ApproveReplyDTO(ReplyManagementDTO):
    pass


class DisapproveReplyDTO(ReplyManagementDTO):
    pass
