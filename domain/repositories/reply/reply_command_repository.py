from abc import ABC, abstractmethod
from typing import List

from domain.dto.reply.internal.reply_command_dto import SetReplyStatusDTO
from domain.dto.reply.internal.reply_filter_dto import ContracteeReplyFilterDTO
from domain.entities.reply.reply import Reply


class ReplyCommandRepository(ABC):
    @abstractmethod
    async def create_reply(self, reply: Reply) -> Reply:
        pass

    @abstractmethod
    async def set_reply_status(self, query: SetReplyStatusDTO) -> Reply:
        pass

    @abstractmethod
    async def drop_replies(
        self, query: ContracteeReplyFilterDTO
    ) -> List[Reply]:
        pass
