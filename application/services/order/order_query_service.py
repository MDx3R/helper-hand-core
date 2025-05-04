from typing import List

from application.usecases.order.order_query_use_case import (
    ListAdminOrdersUseCase,
    ListContracteeOrdersUseCase,
    ListContractorOrdersUseCase,
)
from domain.dto.order.internal.order_filter_dto import OrderFilterDTO
from domain.dto.order.internal.order_query_dto import GetUserOrdersDTO
from domain.dto.order.response.order_output_dto import OrderOutputDTO
from domain.services.order.order_query_service import (
    OrderQueryService,
    UserAssociatedOrderQueryService,
)


class OrderQueryServiceImpl(OrderQueryService):
    def __init__(self):
        # TODO: UseCase
        ...

    async def filter_orders(
        self, query: OrderFilterDTO
    ) -> List[OrderOutputDTO]:
        pass


class UserAssociatedOrderQueryServiceImpl(UserAssociatedOrderQueryService):
    def __init__(
        self,
        list_contractee_orders_use_case: ListContracteeOrdersUseCase,
        list_contractor_orders_use_case: ListContractorOrdersUseCase,
        list_admin_orders_use_case: ListAdminOrdersUseCase,
    ):
        self.list_contractee_orders_use_case = list_contractee_orders_use_case
        self.list_contractor_orders_use_case = list_contractor_orders_use_case
        self.list_admin_orders_use_case = list_admin_orders_use_case

    async def get_contractee_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderOutputDTO]:
        return await self.list_contractee_orders_use_case.execute(query)

    async def get_contractor_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderOutputDTO]:
        return await self.list_contractor_orders_use_case.execute(query)

    async def get_admin_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderOutputDTO]:
        return await self.list_admin_orders_use_case.execute(query)
