from abc import ABC, abstractmethod
from typing import List

from domain.dto.order.internal.base import DetailIdDTO, OrderIdDTO
from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.reply.internal.reply_filter_dto import (
    CountRepliesDTO,
    ReplyFilterDTO,
)
from domain.entities.reply.available_replies_for_detail import (
    AvailableRepliesForDetail,
)
from domain.entities.reply.reply import Reply


class ReplyQueryRepository(ABC):
    @abstractmethod
    async def get_reply(self, query: ReplyIdDTO) -> Reply | None:
        pass

    @abstractmethod
    async def filter_replies(self, query: ReplyFilterDTO) -> List[Reply]:
        pass

    @abstractmethod
    async def get_detail_available_replies_count(
        self, query: DetailIdDTO
    ) -> AvailableRepliesForDetail:
        pass

    @abstractmethod
    async def get_order_available_replies_count(
        self, query: OrderIdDTO
    ) -> List[AvailableRepliesForDetail]:
        pass

    @abstractmethod
    async def count_replies(self, query: CountRepliesDTO) -> int:
        pass
