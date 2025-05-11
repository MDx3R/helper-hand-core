from abc import ABC, abstractmethod
from datetime import date
from typing import List

from domain.dto.order.internal.order_query_dto import GetUserOrderDTO
from domain.dto.reply.internal.reply_filter_dto import (
    ContracteeReplyFilterDTO,
    RepliedContracteesFilterDTO,
)
from domain.entities.reply.reply import Reply
from domain.entities.user.contractee.contractee import Contractee


class ContracteeReplyQueryRepository(ABC):
    @abstractmethod
    async def get_contractees(
        self, query: RepliedContracteesFilterDTO
    ) -> List[Contractee]:
        pass

    @abstractmethod
    async def get_contractee_future_replies(
        self, user_id: int  # TODO: Пагинация
    ) -> List[Reply]:
        # NOTE: !dropped, status == accepted, date >= now() descending by date
        pass

    @abstractmethod
    async def get_contractee_order_replies(
        self, query: GetUserOrderDTO
    ) -> List[Reply]:
        pass

    @abstractmethod
    async def get_contractee_future_busy_dates(
        self, user_id: int
    ) -> List[date]:
        pass

    @abstractmethod
    async def contractee_has_reply(
        self, query: ContracteeReplyFilterDTO
    ) -> bool:
        pass
