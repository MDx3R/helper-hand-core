from dataclasses import dataclass
from typing import List, Optional
from application.transactions import transactional
from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.dto.order.internal.order_query_dto import (
    GetOrderAfterDTO,
    GetOrderDTO,
)
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderDetailOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)
from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.user.internal.user_context_dto import PaginatedDTO
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
        self, detail: OrderDetailOutputDTO, contractee: ContracteeOutputDTO
    ) -> bool:
        if not OrderDetailDomainService.is_relevant_at_current_time(detail):
            return False

        if not OrderDetailDomainService.is_suitable(detail, contractee):
            return False

        return True


class GetUnavailableDetailsForContracteeUseCase:
    def __init__(
        self,
        reply_repository: CompositeReplyQueryRepository,
    ):
        self.reply_repository = reply_repository

    async def execute(self, user_id: int) -> UnavailableDetails:
        replies = await self._get_contractee_replies(user_id)
        return UnavailableDetails(
            details=self._to_detail_ids(replies),
            intervals=self._to_busy_intervals(replies),
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


class GetSuitableDetailsForOrderUseCase:
    def __init__(
        self,
        order_repository: CompositeOrderQueryRepository,
        reply_repository: CompositeReplyQueryRepository,
        contractee_repository: ContracteeQueryRepository,
        unavailable_details_use_case: GetUnavailableDetailsForContracteeUseCase,
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


class ListSuitableOrdersUseCase:
    SIZE = 25

    def __init__(
        self,
        order_repository: CompositeOrderQueryRepository,
        contractee_repository: ContracteeQueryRepository,
        filtering_use_case: GetSuitableDetailsFromOrderUseCase,
        unavailable_details_use_case: GetUnavailableDetailsForContracteeUseCase,
    ):
        self.order_repository = order_repository
        self.contractee_repository = contractee_repository
        self.filtering_use_case = filtering_use_case
        self.unavailable_details_use_case = unavailable_details_use_case

    @transactional
    async def execute(
        self, query: PaginatedDTO
    ) -> List[OrderWithDetailsOutputDTO]:
        taken = await self.unavailable_details_use_case.execute(
            query.context.user_id
        )
        contractee = await self._get_contractee(query.context.user_id)
        return await self._get_suitable_orders(query, taken, contractee)

    async def _get_contractee(self, user_id: int) -> Contractee:
        contractee = await self.contractee_repository.get_contractee(user_id)
        if not contractee:
            # Не должно подниматься
            raise NotFoundException(user_id)
        return contractee

    async def _get_suitable_orders(
        self,
        query: PaginatedDTO,
        taken: UnavailableDetails,
        contractee: Contractee,
    ) -> List[OrderWithDetailsOutputDTO]:
        result = []
        last_id = query.last_id
        while True and len(result) <= query.size:
            orders = await self.order_repository.filter_orders_with_details(
                self._build_filter(last_id)
            )
            if not orders:
                break

            orders = await self._select_suitable_orders(
                orders, taken, contractee
            )
            if orders:
                last_id = orders[-1].order.order_id
                result.extend(orders)

        return result

    def _build_filter(self, last_id: Optional[int]) -> OrderFilterDTO:
        return OrderFilterDTO(
            last_id=last_id,
            status=OrderStatusEnum.open,
            only_available_details=True,
            size=self.SIZE,
        )

    async def _select_suitable_orders(
        self,
        orders: List[OrderWithDetails],
        taken: UnavailableDetails,
        contractee: Contractee,
    ) -> List[OrderWithDetailsOutputDTO]:
        result = []
        for order in orders:
            order_dto = OrderMapper.to_output_with_details(order)
            contractee_dto = ContracteeMapper.to_output(contractee)
            details = self.filtering_use_case.execute(
                CheckOrderSuits(
                    order=order_dto,
                    contractee=contractee_dto,
                    taken=taken,
                )
            )
            if details:
                order_dto.details = details
                result.append(order_dto)
        return result


# TODO: DTO с доступными позициями/Отправлять только доступные позиции
class GetSuitableOrderUseCase:
    def __init__(
        self,
        list_suitable_orders_use_case: ListSuitableOrdersUseCase,
        order_repository: CompositeOrderQueryRepository,
    ):
        self.list_suitable_orders_use_case = list_suitable_orders_use_case
        self.order_repository = order_repository

    @transactional
    async def execute(
        self, query: GetOrderAfterDTO
    ) -> CompleteOrderOutputDTO | None:
        result = await self.list_suitable_orders_use_case.execute(
            PaginatedDTO(last_id=query.last_id, size=1, context=query.context)
        )
        if not result:
            return None
        order_with_details = result[0]

        complete_order = await self.order_repository.get_complete_order(
            order_with_details.order.order_id
        )
        if not complete_order:
            raise

        output = OrderMapper.to_complete(complete_order)
        output.details = order_with_details.details
        return output
