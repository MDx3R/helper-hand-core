from application.transactions import transactional
from domain.dto.order.internal.base import OrderIdDTO
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.reply.internal.reply_query_dto import GetOrderReplyDTO
from domain.dto.reply.response.reply_output_dto import (
    CompleteReplyOutputDTO,
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


class GetPendingReplyForOrderUseCase:
    def __init__(
        self,
        order_repository: OrderQueryRepository,
        reply_repository: CompositeReplyQueryRepository,
    ):
        self.order_repository = order_repository
        self.reply_repository = reply_repository

    @transactional
    async def execute(
        self, query: GetOrderReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        order = await self.order_repository.get_order(query.order_id)
        if not order:
            return None

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
                order_id=query.order_id, status=ReplyStatusEnum.created, size=1
            )
        )
        if not replies:
            return None

        return ReplyMapper.to_complete(replies[0])
