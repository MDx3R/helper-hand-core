from typing import List

from sqlalchemy import Select

from domain.dto.reply.internal.base import ReplyIdDTO
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.entities.reply.composite_reply import (
    CompleteReply,
    ReplyWithDetail,
)
from domain.repositories.reply.composite_reply_query_repository import (
    CompositeReplyQueryRepository,
)
from infrastructure.database.mappers import (
    CompleteReplyMapper,
    ReplyWithDetailMapper,
)
from infrastructure.repositories.base import QueryExecutor
from infrastructure.repositories.reply.base import (
    ReplyQueryBuilder,
    UnmappedReply,
)


class CompositeReplyQueryRepositoryImpl(CompositeReplyQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_complete_reply(
        self, query: ReplyIdDTO
    ) -> CompleteReply | None:
        stmt = (
            self._get_complete_reply_builder()
            .where_reply_id(query.contractee_id, query.detail_id)
            .build()
        )

        unmapped = await self._execute_one(stmt)
        if not unmapped:
            return None

        return CompleteReplyMapper.to_model(
            unmapped.reply,
            unmapped.contractee_user,
            unmapped.contractee,
            unmapped.detail,
            unmapped.order,
        )

    async def filter_complete_replies(
        self, query: ReplyFilterDTO
    ) -> List[CompleteReply]:
        stmt = (
            self._get_complete_reply_builder()
            .apply_reply_filter(query)
            .build()
        )

        result = await self._execute_many(stmt)
        return [
            CompleteReplyMapper.to_model(
                unmapped.reply,
                unmapped.contractee_user,
                unmapped.contractee,
                unmapped.detail,
                unmapped.order,
            )
            for unmapped in result
        ]

    async def filter_replies_with_detail(
        self, query: ReplyFilterDTO
    ) -> List[ReplyWithDetail]:
        stmt = (
            self._get_reply_with_detail_builder()
            .apply_reply_filter(query)
            .build()
        )

        result = await self._execute_many(stmt)
        return [
            ReplyWithDetailMapper.to_model(unmapped.reply, unmapped.detail)
            for unmapped in result
        ]

    def _get_reply_with_detail_builder(self) -> ReplyQueryBuilder:
        return self._get_query_builder().add_detail()

    def _get_complete_reply_builder(self) -> ReplyQueryBuilder:
        return (
            self._get_query_builder().add_contractee().add_detail().add_order()
        )

    def _get_query_builder(self) -> ReplyQueryBuilder:
        return ReplyQueryBuilder()

    async def _execute_one(self, statement: Select) -> UnmappedReply | None:
        row = await self.executor.execute_one(statement)
        if not row:
            return None

        return UnmappedReply(row)

    async def _execute_many(self, statement: Select) -> List[UnmappedReply]:
        result = await self.executor.execute_many(statement)

        return [UnmappedReply(row) for row in result]
