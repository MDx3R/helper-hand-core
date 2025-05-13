from typing import List

from sqlalchemy import select, update

from domain.dto.reply.internal.reply_command_dto import (
    DropReplyDTO,
    SetReplyStatusDTO,
)
from domain.entities.reply.reply import Reply
from domain.repositories.reply.reply_command_repository import (
    ReplyCommandRepository,
)
from infrastructure.database.mappers import ReplyMapper
from infrastructure.database.models import (
    OrderDetailBase,
    ReplyBase,
)
from infrastructure.repositories.base import QueryExecutor


class ReplyCommandRepositoryImpl(ReplyCommandRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def create_reply(self, reply: Reply) -> Reply:
        base = ReplyMapper.to_base(reply)
        await self.executor.add(base)
        return ReplyMapper.to_model(base)

    async def set_reply_status(self, query: SetReplyStatusDTO) -> Reply:
        stmt = (
            update(ReplyBase)
            .where(
                ReplyBase.detail_id == query.detail_id,
                ReplyBase.contractee_id == query.contractee_id,
            )
            .values(status=query.status)
            .returning(ReplyBase)
        )
        reply = await self.executor.execute_scalar_one(stmt)
        return ReplyMapper.to_model(reply)

    async def drop_replies(self, query: DropReplyDTO) -> List[Reply]:
        subquery = select(ReplyBase.reply_id)

        if query.detail_id:
            subquery = subquery.where(ReplyBase.detail_id == query.detail_id)
        if query.contractee_id:
            subquery = subquery.where(
                ReplyBase.contractee_id == query.contractee_id
            )

        if query.date or query.order_id:
            subquery = subquery.join(
                OrderDetailBase,
                ReplyBase.detail_id == OrderDetailBase.detail_id,
            )
            if query.date:
                subquery = subquery.where(OrderDetailBase.date == query.date)
            if query.order_id:
                subquery = subquery.where(
                    OrderDetailBase.order_id == query.order_id
                )

        subquery = subquery.subquery()

        stmt = (
            update(ReplyBase)
            .where(ReplyBase.reply_id.in_(select(subquery.c.reply_id)))
            .values(dropped=True)
            .returning(ReplyBase)
        )

        deleted_replies = await self.executor.execute_scalar_many(stmt)
        return ReplyMapper.to_model_list(deleted_replies)
