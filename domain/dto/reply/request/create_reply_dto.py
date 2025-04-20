from domain.dto.base import ApplicationDTO
from domain.dto.reply.request.reply_input_dto import ReplyInputDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO


class CreateReplyDTO(ApplicationDTO):
    reply: ReplyInputDTO
    context: UserContextDTO
