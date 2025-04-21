from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.entities.reply.enums import ReplyStatusEnum


class SetReplyStatusDTO(ReplyIdDTO):
    status: ReplyStatusEnum


class DropRepliesDTO(ReplyFilterDTO):
    pass
