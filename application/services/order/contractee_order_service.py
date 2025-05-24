from typing import List
from application.services.order.order_query_service import (
    BaseOrderQueryService,
)
from application.usecases.order.contractee.get_order_use_case import (
    GetOrderForContracteeUseCase,
)
from application.usecases.order.contractee.get_suitable_order_use_case import (
    GetSuitableDetailsForOrderUseCase,
    GetSuitableOrderUseCase,
    ListSuitableOrdersUseCase,
)
from application.usecases.order.contractee.list_participated_orders_use_case import (
    ListParticipatedOrdersUseCase,
)
from domain.dto.user.internal.user_context_dto import PaginatedDTO
from domain.services.order.contractee_order_service import (
    ContracteeOrderQueryService,
)
from domain.dto.order.internal.order_query_dto import (
    GetOrderAfterDTO,
    GetOrderDTO,
)
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderDetailOutputDTO,
    OrderWithDetailsOutputDTO,
)


class ContracteeOrderQueryServiceImpl(
    BaseOrderQueryService, ContracteeOrderQueryService
):
    def __init__(
        self,
        get_order_use_case: GetOrderForContracteeUseCase,
        get_orders_use_case: ListParticipatedOrdersUseCase,
        list_suitable_orders_use_case: ListSuitableOrdersUseCase,
        get_suitable_details_use_case: GetSuitableDetailsForOrderUseCase,
    ):
        super().__init__(get_order_use_case, get_orders_use_case)
        self.list_suitable_orders_use_case = list_suitable_orders_use_case
        self.get_suitable_details_use_case = get_suitable_details_use_case

    async def get_suitable_orders(
        self, query: PaginatedDTO
    ) -> List[OrderWithDetailsOutputDTO]:
        return await self.list_suitable_orders_use_case.execute(query)

    async def get_suitable_details_for_order(
        self, query: GetOrderDTO
    ) -> List[OrderDetailOutputDTO]:
        return await self.get_suitable_details_use_case.execute(query)
