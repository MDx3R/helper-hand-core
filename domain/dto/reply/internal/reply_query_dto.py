from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO


class GetReplyDTO(ReplyIdDTO):
    pass


class GetReplyWithContextDTO(ReplyIdDTO):
    context: UserContextDTO
