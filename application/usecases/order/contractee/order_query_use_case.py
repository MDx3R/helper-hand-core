from typing import List

from application.transactions import transactional
from domain.dto.order.internal.order_query_dto import (
    GetOrderDTO,
    GetUserOrderAfterDTO,
    GetUserOrderDTO,
)
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderDetailOutputDTO,
)
from domain.dto.reply.internal.reply_filter_dto import ContracteeReplyFilterDTO
from domain.mappers.order_mappers import OrderMapper
from domain.repositories.order.composite_order_query_repository import (
    CompositeOrderQueryRepository,
)
from domain.repositories.reply.contractee_reply_query_repository import (
    ContracteeReplyQueryRepository,
)
from domain.services.domain.services import OrderDomainService


# TODO: Добавить отклики?
class GetCompleteOrderForContracteeUseCase:
    def __init__(
        self,
        contractee_repository: ContracteeReplyQueryRepository,
        composite_repository: CompositeOrderQueryRepository,
    ):
        self.contractee_repository = contractee_repository
        self.composite_repository = composite_repository

    @transactional
    async def execute(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        complete_order = await self.composite_repository.get_complete_order(
            query
        )
        participated = await self.contractee_repository.contractee_has_reply(
            ContracteeReplyFilterDTO(
                order_id=query.order_id, contractee_id=query.context.user_id
            )
        )
        if not participated and not OrderDomainService.is_available(
            complete_order.order
        ):
            return None

        return OrderMapper.to_complete(complete_order)


# Administrative
# TODO: DTO с доступными позициями/Отправлять только доступные позиции
class GetSuitableOrderUseCase:
    # Заказ всегда подходит, если заказ открыт и подходят сведения -> GetSuitableDetailsUseCase
    async def execute(
        self, query: GetUserOrderAfterDTO
    ) -> CompleteOrderOutputDTO | None:
        pass


# Ridiculously Hard
class GetSuitableDetailsUseCase:
    # Заказ открыт NOTE: Тут?
    # Есть места
    # Подходит по параметрам
    # Нет отклика на дату
    async def execute(
        self, query: GetUserOrderDTO
    ) -> List[OrderDetailOutputDTO]:
        pass


# class GetAvailableOrInvolvedOrderUseCase:
#     def __init__(
#         self,
#         order_repository: OrderRepository,
#         get_order_use_case: GetOrderUseCase,
#         contractee_reply_use_case: HasContracteeRepliedToOrderUseCase,
#     ):
#         self.order_repository = order_repository
#         self.get_order_use_case = get_order_use_case
#         self.contractee_reply_use_case = contractee_reply_use_case

#     async def get_order(self, query: GetUserOrderDTO) -> OrderDTO | None:
#         order = await self.get_order_use_case.get_order(
#             GetOrderDTO(order_id=query.order_id)
#         )
#         if not order:
#             return None

#         if OrderDomainService.is_available(order):
#             return order
#         if self.contractee_reply_use_case.has_contractee_replied(query):
#             return order

#         return None
