from typing import List

from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.dto.order.internal.order_query_dto import (
    GetOrderDTO,
    GetUserOrdersDTO,
)
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)
from domain.dto.user.internal.user_context_dto import (
    PaginatedDTO,
    UserContextDTO,
)
from domain.mappers.order_mappers import OrderMapper
from domain.repositories.order.composite_order_query_repository import (
    CompositeOrderQueryRepository,
)
from domain.repositories.order.order_query_repository import (
    OrderQueryRepository,
)
from domain.services.domain.services import UserDomainService


# Common
class GetOrderUseCase:
    def __init__(
        self,
        repository: OrderQueryRepository,
    ):
        self.repository = repository

    async def execute(self, query: GetOrderDTO) -> OrderOutputDTO | None:
        order = await self.repository.get_order(query)
        if not order:
            return None

        return OrderMapper.to_output(order)


class GetOrderWithDetailsUseCase:
    def __init__(
        self,
        repository: CompositeOrderQueryRepository,
    ):
        self.repository = repository

    async def execute(
        self, query: GetOrderDTO
    ) -> OrderWithDetailsOutputDTO | None:
        order = await self.repository.get_order_with_details(query)
        if not order:
            return None

        return OrderMapper.to_output_with_details(order)


class GetCompleteOrderUseCase:
    def __init__(
        self,
        repository: CompositeOrderQueryRepository,
    ):
        self.repository = repository

    async def execute(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        order = await self.repository.get_complete_order(query)
        if not order:
            return None

        return OrderMapper.to_complete(order)


class GetOrderUseCase:
    def __init__(
        self,
        repository: CompositeOrderQueryRepository,
    ):
        self.repository = repository

    async def execute(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        order = await self.repository.get_complete_order(query)
        if not order:
            return None

        return OrderMapper.to_complete(order)


class ListOrdersUseCase:
    def __init__(
        self,
        repository: OrderQueryRepository,
    ):
        self.repository = repository

    async def execute(self, query: PaginatedDTO) -> List[OrderOutputDTO]:
        orders = await self.repository.filter_orders(self._build_filter(query))

        return [OrderMapper.to_output(i) for i in orders]

    def _build_filter(self, query: PaginatedDTO) -> OrderFilterDTO:
        user = query.context

        params = {
            "last_id": query.last_id,
            "size": query.size,
            "order": "descending",
        }

        if UserDomainService.is_admin(user):
            params.update(admin_id=user.user_id)
        elif UserDomainService.is_contractee(user):
            params.update(contractee_id=user.user_id)
        elif UserDomainService.is_contractor(user):
            params.update(contractor_id=user.user_id)
        else:
            # Не должно вызываться
            raise

        return OrderFilterDTO.model_validate(params)


class ListUserOrdersUseCase:  # TODO: Не думаю, что этот класс имеет смысл, хотя можно для билдинга фильтра получать пользователя
    async def execute(self, query: GetUserOrdersDTO) -> List[OrderOutputDTO]:
        pass


class ListAdminOrdersUseCase:
    def __init__(
        self,
        repository: OrderQueryRepository,
    ):
        self.repository = repository

    async def execute(self, query: GetUserOrdersDTO) -> List[OrderOutputDTO]:
        orders = await self.repository.filter_orders(
            OrderFilterDTO(
                admin_id=query.user_id,
                last_id=query.last_id,
                size=query.size,
                order="descending",
            )
        )

        return [OrderMapper.to_output(i) for i in orders]


class ListContractorOrdersUseCase:
    def __init__(
        self,
        repository: OrderQueryRepository,
    ):
        self.repository = repository

    async def execute(self, query: GetUserOrdersDTO) -> List[OrderOutputDTO]:
        orders = await self.repository.filter_orders(
            OrderFilterDTO(
                contractor_id=query.user_id,
                last_id=query.last_id,
                size=query.size,
                order="descending",
            )
        )

        return [OrderMapper.to_output(i) for i in orders]


class ListContracteeOrdersUseCase:
    def __init__(
        self,
        repository: OrderQueryRepository,
    ):
        self.repository = repository

    async def execute(self, query: GetUserOrdersDTO) -> List[OrderOutputDTO]:
        orders = await self.repository.filter_orders(
            OrderFilterDTO(
                contractee_id=query.user_id,
                last_id=query.last_id,
                size=query.size,
                order="descending",
            )
        )

        return [OrderMapper.to_output(i) for i in orders]
