from typing import List

from domain.dto.base import LastObjectDTO, PaginationDTO, SortingOrder
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
from domain.entities.order.enums import OrderStatusEnum
from domain.entities.user.user import User
from domain.mappers.order_mappers import OrderMapper
from domain.repositories.order.composite_order_query_repository import (
    CompositeOrderQueryRepository,
)
from domain.repositories.order.order_query_repository import (
    OrderQueryRepository,
)
from domain.repositories.user.user_query_repository import UserQueryRepository
from domain.services.domain.services import UserDomainService


# Common
class GetOrderUseCase:
    def __init__(
        self,
        repository: CompositeOrderQueryRepository,
    ):
        self.repository = repository

    async def execute(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        order = await self.repository.get_complete_order(query.order_id)
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


class ListRecentOrdersUseCase:
    def __init__(
        self,
        repository: OrderQueryRepository,
    ):
        self.repository = repository

    async def execute(self, query: PaginationDTO) -> List[OrderOutputDTO]:
        orders = await self.repository.filter_orders(self._build_filter(query))

        return [OrderMapper.to_output(i) for i in orders]

    def _build_filter(self, query: PaginationDTO) -> OrderFilterDTO:
        params = {
            "last_id": query.last_id,
            "size": query.size,
            "status": OrderStatusEnum.open,
            "order": "descending",
        }

        return OrderFilterDTO.model_validate(params)


class ListUserOrdersUseCase:  # TODO: Не думаю, что этот класс имеет смысл, хотя можно для билдинга фильтра получать пользователя
    def __init__(
        self,
        order_repository: OrderQueryRepository,
        user_repository: UserQueryRepository,
    ):
        self.order_repository = order_repository
        self.user_repository = user_repository

    async def execute(self, query: GetUserOrdersDTO) -> List[OrderOutputDTO]:
        user = await self.user_repository.get_user(query.user_id)
        if not user:
            return []

        orders = await self.order_repository.filter_orders(
            self._build_filter(user, query)
        )

        return [OrderMapper.to_output(i) for i in orders]

    def _build_filter(
        self, user: User, query: GetUserOrdersDTO
    ) -> OrderFilterDTO:
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
                sorting=SortingOrder.descending,
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
                sorting=SortingOrder.descending,
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
                sorting=SortingOrder.descending,
            )
        )

        return [OrderMapper.to_output(i) for i in orders]
