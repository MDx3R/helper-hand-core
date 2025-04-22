from abc import ABC, abstractmethod
from typing import List

from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.entities.reply.detailed_reply import CompleteReply


class CompositeReplyQueryRepository(ABC):
    @abstractmethod
    async def get_complete_reply(
        self, query: ReplyIdDTO
    ) -> CompleteReply | None:
        pass

    @abstractmethod
    async def filter_complete_replies(
        self, query: ReplyFilterDTO
    ) -> List[CompleteReply]:
        pass
