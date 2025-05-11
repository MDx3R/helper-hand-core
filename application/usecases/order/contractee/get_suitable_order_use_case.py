from dataclasses import dataclass
from typing import List
from application.transactions import transactional
from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.dto.order.internal.order_query_dto import (
    GetOrderAfterDTO,
    GetOrderDTO,
)
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderDetailOutputDTO,
    OrderWithDetailsOutputDTO,
)
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
)
from domain.entities.order.composite_order import (
    CompleteOrder,
    OrderWithDetails,
)
from domain.entities.order.detail import OrderDetail, TimeInterval
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.reply.composite_reply import ReplyWithDetail
from domain.entities.user.contractee.contractee import Contractee
from domain.exceptions.service.common import NotFoundException
from domain.mappers.order_mappers import OrderDetailMapper, OrderMapper
from domain.mappers.user_mappers import ContracteeMapper
from domain.repositories.order.composite_order_query_repository import (
    CompositeOrderQueryRepository,
)
from domain.repositories.reply.composite_reply_query_repository import (
    CompositeReplyQueryRepository,
)
from domain.repositories.user.contractee.contractee_query_repository import (
    ContracteeQueryRepository,
)
from domain.services.domain.services import (
    OrderDetailDomainService,
    OrderDomainService,
    ReplyDomainService,
)


@dataclass
class UnavailableDetails:
    details: List[int]
    intervals: List[TimeInterval]


@dataclass
class CheckOrderSuits:
    order: OrderWithDetailsOutputDTO
    contractee: ContracteeOutputDTO
    taken: UnavailableDetails


class GetSuitableDetailsFromOrderUseCase:
    def execute(self, query: CheckOrderSuits) -> List[OrderDetailOutputDTO]:
        composite_order = query.order
        details = composite_order.details

        if not details or not OrderDomainService.can_have_replies(
            composite_order.order
        ):
            return []

        taken_details = query.taken.details
        busy_intervals = query.taken.intervals
        filtered_details = []
        for detail in details:
            if detail.detail_id in taken_details:
                continue
            if any(
                interval.contains(detail.start_date)
                for interval in busy_intervals
            ):
                continue
            if self._is_detail_suitable(detail, query.contractee):
                filtered_details.append(detail)

        return [
            OrderDetailMapper.to_output(detail) for detail in filtered_details
        ]

    def _is_detail_suitable(
        self, detail: OrderDetail, contractee: Contractee
    ) -> bool:
        if not OrderDetailDomainService.is_relevant_at_current_time(detail):
            return False

        if not OrderDetailDomainService.is_suitable(detail, contractee):
            return False

        return True


class GetUnavailableDetailsForContractee:
    def __init__(
        self,
        reply_repository: CompositeReplyQueryRepository,
    ):
        self.reply_repository = reply_repository

    async def execute(self, user_id: int) -> UnavailableDetails:
        replies = await self._get_contractee_replies(user_id)
        return UnavailableDetails(
            taken_details=self._to_detail_ids(replies),
            taken_intervals=self._to_busy_intervals(replies),
        )

    async def _get_contractee_replies(
        self, user_id: int
    ) -> List[ReplyWithDetail]:
        return await self.reply_repository.filter_replies_with_detail(
            ReplyFilterDTO(
                contractee_id=user_id,
                starts_after=OrderDetailDomainService.get_latest_allowed_start_time(),
            )
        )

    def _to_detail_ids(self, replies: List[ReplyWithDetail]) -> List[int]:
        return [reply.reply.detail_id for reply in replies]

    def _to_busy_intervals(
        self, replies: List[ReplyWithDetail]
    ) -> List[TimeInterval]:
        return [
            reply.detail.inteval
            for reply in replies
            if ReplyDomainService.is_future_or_ongoing(
                reply.reply, reply.detail
            )
        ]


class GetSuitableDetailsUseCase:
    def __init__(
        self,
        order_repository: CompositeOrderQueryRepository,
        reply_repository: CompositeReplyQueryRepository,
        contractee_repository: ContracteeQueryRepository,
        unavailable_details_use_case: GetUnavailableDetailsForContractee,
        filtering_use_case: GetSuitableDetailsFromOrderUseCase,
    ):
        self.order_repository = order_repository
        self.reply_repository = reply_repository
        self.contractee_repository = contractee_repository
        self.unavailable_details_use_case = unavailable_details_use_case
        self.filtering_use_case = filtering_use_case

    @transactional
    async def execute(self, query: GetOrderDTO) -> List[OrderDetailOutputDTO]:
        composite_order = await self._get_order_with_details(query.order_id)
        if not OrderDomainService.can_have_replies(composite_order.order):
            return []

        contractee = await self._get_contractee(query.context.user_id)

        taken = await self.unavailable_details_use_case.execute(
            contractee.user_id
        )
        details = self.filtering_use_case.execute(
            CheckOrderSuits(
                order=OrderMapper.to_output_with_details(composite_order),
                contractee=ContracteeMapper.to_output(contractee),
                taken=taken,
            )
        )

        return details

    async def _get_order_with_details(self, order_id: int) -> OrderWithDetails:
        order = await self.order_repository.get_order_with_free_details(
            order_id
        )
        if not order:
            raise NotFoundException(order_id)
        return order

    async def _get_contractee(self, user_id: int) -> Contractee:
        contractee = await self.contractee_repository.get_contractee(user_id)
        if not contractee:
            # Не должно подниматься
            raise NotFoundException(user_id)
        return contractee


# TODO: DTO с доступными позициями/Отправлять только доступные позиции
class GetSuitableOrderUseCase:
    def __init__(
        self,
        order_repository: CompositeOrderQueryRepository,
        contractee_repository: ContracteeQueryRepository,
        filtering_use_case: GetSuitableDetailsFromOrderUseCase,
        unavailable_details_use_case: GetUnavailableDetailsForContractee,
    ):
        self.order_repository = order_repository
        self.contractee_repository = contractee_repository
        self.filtering_use_case = filtering_use_case
        self.unavailable_details_use_case = unavailable_details_use_case

    @transactional
    async def execute(
        self, query: GetOrderAfterDTO
    ) -> CompleteOrderOutputDTO | None:
        taken = await self.unavailable_details_use_case.execute(
            query.context.user_id
        )
        contractee = await self._get_contractee(query.context.user_id)

        last_id = query.last_id
        while True:
            orders = await self.order_repository.filter_complete_orders(
                self._build_filter(last_id)
            )
            if not orders:
                break

            order = await self._select_suitable_order(
                orders, taken, contractee
            )
            if order:
                return OrderMapper.to_complete(order)

            last_id = orders[-1].order.order_id

        return None

    async def _get_contractee(self, user_id: int) -> Contractee:
        contractee = await self.contractee_repository.get_contractee(user_id)
        if not contractee:
            # Не должно подниматься
            raise NotFoundException(user_id)
        return contractee

    def _build_filter(self, last_id: int) -> OrderFilterDTO:
        return OrderFilterDTO(
            last_id=last_id,
            status=OrderStatusEnum.open,
            only_available_details=True,
        )

    async def _select_suitable_order(
        self,
        orders: List[CompleteOrder],
        taken: UnavailableDetails,
        contractee: ContracteeOutputDTO,
    ) -> CompleteOrderOutputDTO | None:
        for order in orders:
            order_dto = OrderMapper.to_complete(order)
            details = self.filtering_use_case.execute(
                CheckOrderSuits(
                    order=order_dto,
                    contractee=contractee,
                    taken=taken,
                )
            )
            if details:
                order_dto.details = details
                return order_dto
        return None
