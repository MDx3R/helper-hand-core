from domain.dto.reply.base import ReplyBaseDTO
from domain.entities.reply.enums import ReplyStatusEnum


class ReplyOutputDTO(ReplyBaseDTO):
    status: ReplyStatusEnum
