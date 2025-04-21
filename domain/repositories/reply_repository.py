from abc import ABC, abstractmethod
from datetime import date
from typing import List

from domain.dto.order.internal.base import DetailIdDTO, OrderIdDTO
from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.reply.internal.reply_command_dto import (
    DropRepliesDTO,
    SetReplyStatusDTO,
)
from domain.dto.reply.internal.reply_filter_dto import (
    ContracteeReplyFilterDTO,
    CountRepliesDTO,
    RepliedContracteesFilterDTO,
    ReplyFilterDTO,
)
from domain.dto.user.internal.base import UserIdDTO
from domain.entities.reply.available_replies_for_detail import (
    AvailableRepliesForDetail,
)
from domain.entities.reply.detailed_reply import CompleteReply
from domain.entities.reply.reply import Reply
from domain.entities.user.contractee import Contractee


class ReplyQueryRepository(ABC):
    @abstractmethod
    async def get_reply(self, query: ReplyIdDTO) -> Reply | None:
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


class ContracteeReplyQueryRepository(ABC):
    @abstractmethod
    async def get_contractees(
        self, query: RepliedContracteesFilterDTO
    ) -> List[Contractee]:
        pass

    @abstractmethod
    async def get_contractee_future_replies(
        self, query: UserIdDTO
    ) -> List[Reply]:
        pass

    @abstractmethod
    async def get_contractee_future_busy_dates(
        self, query: UserIdDTO
    ) -> List[date]:
        pass

    @abstractmethod
    async def contractee_has_reply(
        self, query: ContracteeReplyFilterDTO
    ) -> bool:
        pass


class ReplyCommandRepository(ABC):
    @abstractmethod
    async def create_reply(self, reply: Reply) -> Reply:
        pass

    @abstractmethod
    async def set_reply_status(self, query: SetReplyStatusDTO) -> Reply:
        pass

    @abstractmethod
    async def drop_replies(self, query: DropRepliesDTO) -> List[Contractee]:
        pass
