from typing import List
from application.transactions import transactional
from domain.dto.order.internal.base import OrderIdDTO
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.reply.internal.reply_query_dto import (
    GetOrderRepliesDTO,
    GetOrderReplyDTO,
)
from domain.dto.reply.response.reply_output_dto import (
    CompleteReplyOutputDTO,
)
from domain.dto.user.internal.user_context_dto import (
    PaginatedDTO,
    UserContextDTO,
)
from domain.entities.reply.enums import ReplyStatusEnum
from domain.exceptions.service.auth import UnauthorizedAccessException
from domain.exceptions.service.orders import OrderActionNotAllowedException
from domain.mappers.reply_mappers import ReplyMapper
from domain.repositories.order.order_query_repository import (
    OrderQueryRepository,
)
from domain.repositories.reply.composite_reply_query_repository import (
    CompositeReplyQueryRepository,
)
from domain.services.domain.services import OrderDomainService


class ListPendingRepliesForOrderUseCase:
    def __init__(
        self,
        order_repository: OrderQueryRepository,
        reply_repository: CompositeReplyQueryRepository,
    ):
        self.order_repository = order_repository
        self.reply_repository = reply_repository

    @transactional
    async def execute(
        self, query: GetOrderRepliesDTO
    ) -> List[CompleteReplyOutputDTO]:
        order = await self.order_repository.get_order(query.order_id)
        if not order:
            return []

        if not OrderDomainService.is_owned_by(order, query.context.user_id):
            raise UnauthorizedAccessException()

        if not OrderDomainService.can_have_replies(order):
            raise OrderActionNotAllowedException(
                order.order_id,
                order.status,
                "Получить неподтвержденный отклик",
            )

        replies = await self.reply_repository.filter_complete_replies(
            ReplyFilterDTO(
                order_id=query.order_id,
                status=ReplyStatusEnum.created,
                dropped=False,
                size=query.size,
                last_id=query.last_id,
            )
        )

        return [ReplyMapper.to_complete(i) for i in replies]


class GetPendingReplyForOrderUseCase:
    def __init__(
        self,
        list_pending_replies_use_case: ListPendingRepliesForOrderUseCase,
    ):
        self.list_pending_replies_use_case = list_pending_replies_use_case

    async def execute(
        self, query: GetOrderReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        replies = await self.list_pending_replies_use_case.execute(
            GetOrderRepliesDTO(
                context=query.context, order_id=query.order_id, size=1
            )
        )
        if not replies:
            return None

        return replies[0]


class ListPendingRepliesUseCase:
    def __init__(
        self,
        order_repository: OrderQueryRepository,
        reply_repository: CompositeReplyQueryRepository,
    ):
        self.order_repository = order_repository
        self.reply_repository = reply_repository

    async def execute(
        self, query: PaginatedDTO
    ) -> List[CompleteReplyOutputDTO]:
        replies = await self.reply_repository.filter_complete_replies(
            ReplyFilterDTO(
                contractor_id=query.context.user_id,
                status=ReplyStatusEnum.created,
                dropped=False,
                size=query.size,
                last_id=query.last_id,
            )
        )

        return [ReplyMapper.to_complete(i) for i in replies]


class GetPendingReplyUseCase:
    def __init__(
        self,
        list_pending_replies_use_case: ListPendingRepliesUseCase,
    ):
        self.list_pending_replies_use_case = list_pending_replies_use_case

    async def execute(
        self, context: UserContextDTO
    ) -> CompleteReplyOutputDTO | None:
        replies = await self.list_pending_replies_use_case.execute(
            PaginatedDTO(context=context, size=1)
        )
        if not replies:
            return None

        return replies[0]
