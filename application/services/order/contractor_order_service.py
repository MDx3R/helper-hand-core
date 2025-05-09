from ast import List
from application.external.notification.notification_service import (
    AdminOrderNotificationService,
    ContracteeOrderNotificationService,
)
from application.services.order.order_query_service import (
    BaseOrderQueryService,
)
from application.usecases.order.change_order_status_use_case import (
    CancelOrderUseCase,
    SetActiveOrderUseCase,
)
from application.usecases.order.contractor.create_order_use_case import (
    CreateOrderForContractorUseCase,
)
from application.usecases.order.contractor.get_order_use_case import (
    GetOrderForContractorUseCase,
)
from application.usecases.order.contractor.list_owned_orders_use_case import (
    ListOwnedOrdersUseCase,
)
from domain.dto.order.internal.order_managment_dto import (
    CancelOrderDTO,
    SetOrderActiveDTO,
)
from domain.dto.order.internal.order_query_dto import GetOrderDTO
from domain.dto.order.request.create_order_dto import CreateOrderDTO
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)
from domain.dto.user.internal.user_context_dto import PaginatedDTO
from domain.services.domain.services import OrderDomainService
from domain.services.order.contractor_order_service import (
    ContractorOrderManagementService,
    ContractorOrderQueryService,
)


class ContractorOrderManagementServiceImpl(ContractorOrderManagementService):
    def __init__(
        self,
        create_order_use_case: CreateOrderForContractorUseCase,
        cancel_order_use_case: CancelOrderUseCase,
        set_order_active_use_case: SetActiveOrderUseCase,
        admin_notification_service: AdminOrderNotificationService,
        contractee_notification_service: ContracteeOrderNotificationService,
    ):
        self.create_order_use_case = create_order_use_case
        self.cancel_order_use_case = cancel_order_use_case
        self.set_order_active_use_case = set_order_active_use_case

        self.admin_notification_service = admin_notification_service
        self.contractee_notification_service = contractee_notification_service

    async def create_order(
        self, request: CreateOrderDTO
    ) -> OrderWithDetailsOutputDTO:
        order = await self.create_order_use_case.execute(request)
        await self.admin_notification_service.send_order_cancelled_notification()  # TODO: DTO
        return order

    async def cancel_order(self, request: CancelOrderDTO) -> OrderOutputDTO:
        order = await self.cancel_order_use_case.execute(request)
        if OrderDomainService.has_supervisor(order):
            await self.admin_notification_service.send_order_cancelled_notification()  # TODO: DTO
        await self.contractee_notification_service.send_order_cancelled_notification()  # TODO: DTO
        return order

    async def set_order_active(
        self, request: SetOrderActiveDTO
    ) -> OrderOutputDTO:
        order = await self.set_order_active_use_case.execute(request)
        await self.admin_notification_service.send_order_set_active_notification()  # TODO: DTO
        await self.contractee_notification_service.send_order_cancelled_notification()  # TODO: DTO
        return order


class ContractorOrderQueryServiceImpl(
    ContractorOrderQueryService, BaseOrderQueryService
):
    def __init__(
        self,
        get_order_use_case: GetOrderForContractorUseCase,
        get_orders_use_case: ListOwnedOrdersUseCase,
    ):
        super().__init__(get_order_use_case, get_orders_use_case)
