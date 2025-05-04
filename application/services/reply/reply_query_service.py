from abc import ABC, abstractmethod
from typing import List

from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO
from domain.services.reply.reply_query_service import ReplyQueryService


class ReplyQueryServiceImpl(ReplyQueryService):
    def __init__(self):
        # TODO: UseCase
        ...

    async def filter_replies(
        self, query: ReplyFilterDTO
    ) -> List[ReplyOutputDTO]:
        pass
