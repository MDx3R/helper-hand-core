from typing import List
from application.usecases.order.contractee.order_query_use_case import (
    GetCompleteOrderForContracteeUseCase,
    GetSuitableDetailsUseCase,
    GetSuitableOrderUseCase,
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


class ContracteeOrderQueryServiceImpl(ContracteeOrderQueryService):
    def __init__(
        self,
        get_order_use_case: GetCompleteOrderForContracteeUseCase,
        get_suitable_order_use_case: GetSuitableOrderUseCase,
        get_suitable_details_use_case: GetSuitableDetailsUseCase,
    ):
        self.get_order_use_case = get_order_use_case
        self.get_suitable_order_use_case = get_suitable_order_use_case
        self.get_suitable_details_use_case = get_suitable_details_use_case

    async def get_order(
        self, query: GetOrderDTO
    ) -> CompleteOrderOutputDTO | None:
        return await self.get_order_use_case.execute(query)

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
