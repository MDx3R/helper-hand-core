from application.transactions import transactional
from application.usecases.reply.reply_query_use_case import GetReplyUseCase
from domain.dto.order.internal.base import DetailIdDTO, OrderIdDTO
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.reply.internal.reply_query_dto import (
    GetOrderReplyDTO,
    GetReplyDTO,
)
from domain.dto.reply.response.reply_output_dto import (
    CompleteReplyOutputDTO,
)
from domain.entities.order.order import Order
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


# Common
class GetReplyForContractorUseCase(GetReplyUseCase):
    def __init__(
        self,
        order_repository: OrderQueryRepository,
        reply_repository: CompositeReplyQueryRepository,
    ):
        super().__init__(reply_repository)
        self.order_repository = order_repository

    @transactional
    async def execute(
        self, query: GetReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        order = await self.order_repository.get_order_for_detail(
            query.detail_id
        )

        if not order or not OrderDomainService.is_owned_by(
            order, query.context.user_id
        ):
            return None

        return await super().execute(query)
