from abc import ABC, abstractmethod
from datetime import date
from typing import List

from domain.dto.reply.internal.reply_filter_dto import (
    ContracteeReplyFilterDTO,
    RepliedContracteesFilterDTO,
)
from domain.dto.user.internal.base import UserIdDTO
from domain.entities.reply.reply import Reply
from domain.entities.user.contractee import Contractee


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
