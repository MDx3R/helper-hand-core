from typing import List
from application.services.order.order_query_service import (
    BaseOrderQueryService,
)
from application.usecases.order.contractee.get_order_use_case import (
    GetOrderForContracteeUseCase,
)
from application.usecases.order.contractee.get_suitable_order_use_case import (
    GetSuitableDetailsUseCase,
    GetSuitableOrderUseCase,
)
from application.usecases.order.contractee.list_participated_orders_use_case import (
    ListParticipatedOrdersUseCase,
)
from domain.services.order.contractee_order_service import (
    ContracteeOrderQueryService,
)
from domain.dto.order.internal.order_query_dto import (
    GetOrderAfterDTO,
    GetOrderDTO,
    GetUserOrderAfterDTO,
    GetUserOrderDTO,
)
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderDetailOutputDTO,
)


class ContracteeOrderQueryServiceImpl(
    ContracteeOrderQueryService, BaseOrderQueryService
):
    def __init__(
        self,
        get_order_use_case: GetOrderForContracteeUseCase,
        get_orders_use_case: ListParticipatedOrdersUseCase,
        get_suitable_order_use_case: GetSuitableOrderUseCase,
        get_suitable_details_use_case: GetSuitableDetailsUseCase,
    ):
        super().__init__(get_order_use_case, get_orders_use_case)
        self.get_suitable_order_use_case = get_suitable_order_use_case
        self.get_suitable_details_use_case = get_suitable_details_use_case

    async def get_suitable_order(
        self, query: GetOrderAfterDTO
    ) -> CompleteOrderOutputDTO | None:
        return await self.get_suitable_order_use_case.execute(
            GetUserOrderAfterDTO(
                last_id=query.last_id, user_id=query.context.user_id
            )
        )

    async def get_suitable_details(
        self, query: GetOrderDTO
    ) -> List[OrderDetailOutputDTO]:
        return await self.get_suitable_details_use_case.execute(
            GetUserOrderDTO(
                order_id=query.order_id, user_id=query.context.user_id
            )
        )
