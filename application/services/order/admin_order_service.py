from typing import List
from application.external.notification.notification_service import (
    ContracteeOrderNotificationService,
    ContractorOrderNotificationService,
)
from application.services.order.order_query_service import (
    BaseOrderQueryService,
)
from application.usecases.order.admin.create_order_use_case import (
    CreateOrderForAdminUseCase,
)
from application.usecases.order.admin.get_order_use_case import (
    GetOrderForAdminUseCase,
)
from application.usecases.order.admin.get_unassigned_order_use_case import (
    GetUnassignedOrderUseCase,
)
from application.usecases.order.admin.list_supervised_orders_use_case import (
    ListSupervisedOrdersUseCase,
)
from application.usecases.order.admin.take_order_use_case import (
    TakeOrderUseCase,
)
from application.usecases.order.change_order_status_use_case import (
    ApproveOrderUseCase,
    CancelOrderUseCase,
    CloseOrderUseCase,
    DisapproveOrderUseCase,
    FulfillOrderUseCase,
    OpenOrderUseCase,
)
from domain.dto.base import LastObjectDTO
from domain.dto.order.internal.order_managment_dto import (
    ApproveOrderDTO,
    CancelOrderDTO,
    CloseOrderDTO,
    DisapproveOrderDTO,
    FulfillOrderDTO,
    OpenOrderDTO,
    TakeOrderDTO,
)
from domain.dto.order.internal.order_query_dto import (
    GetOrderDTO,
    GetUserOrdersDTO,
)
from domain.dto.order.request.create_order_dto import CreateOrderDTO
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)
from domain.dto.user.internal.user_context_dto import PaginatedDTO
from domain.services.domain.services import OrderDomainService
from domain.services.order.admin_order_service import (
    AdminOrderManagementService,
    AdminOrderQueryService,
)


class AdminOrderManagementServiceImpl(AdminOrderManagementService):
    def __init__(
        self,
        create_order_use_case: CreateOrderForAdminUseCase,
        take_order_use_case: TakeOrderUseCase,
        approve_order_use_case: ApproveOrderUseCase,
        disapprove_order_use_case: DisapproveOrderUseCase,
        cancel_order_use_case: CancelOrderUseCase,
        close_order_use_case: CloseOrderUseCase,
        open_order_use_case: OpenOrderUseCase,
        fulfill_order_use_case: FulfillOrderUseCase,
        contractee_notification_service: ContracteeOrderNotificationService,
        contractor_notification_service: ContractorOrderNotificationService,
    ):
        self.create_order_use_case = create_order_use_case
        self.take_order_use_case = take_order_use_case
        self.approve_order_use_case = approve_order_use_case
        self.disapprove_order_use_case = disapprove_order_use_case
        self.cancel_order_use_case = cancel_order_use_case
        self.close_order_use_case = close_order_use_case
        self.open_order_use_case = open_order_use_case
        self.fulfill_order_use_case = fulfill_order_use_case

        self.contractee_notification_service = contractee_notification_service
        self.contractor_notification_service = contractor_notification_service

    async def create_order(
        self, request: CreateOrderDTO
    ) -> OrderWithDetailsOutputDTO:
        order = await self.create_order_use_case.execute(request)
        await self.contractee_notification_service.send_new_order_notification()  # TODO: DTO
        return order

    async def take_order(self, request: TakeOrderDTO) -> OrderOutputDTO:
        order = await self.take_order_use_case.execute(request)
        # Проверка на владение заказа не имеет смысла, так как подразумевается,
        # что заказ, созданный админом, не может быть заново подтвежден
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            await self.contractor_notification_service.send_admin_assigned_notification()  # TODO: DTO
        return order

    async def approve_order(self, request: ApproveOrderDTO) -> OrderOutputDTO:
        order = await self.approve_order_use_case.execute(request)
        # Проверка на владение заказа не имеет смысла, так как подразумевается,
        # что заказ, созданный админом, не может быть заново подтвежден
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            await self.contractor_notification_service.send_order_approved_notification()  # TODO: DTO
        return order

    async def disapprove_order(
        self, request: DisapproveOrderDTO
    ) -> OrderOutputDTO:
        order = await self.disapprove_order_use_case.execute(request)
        # Проверка на владение заказа не имеет смысла, так как подразумевается,
        # что заказ, созданный админом, не может быть заново подтвежден
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            await self.contractor_notification_service.send_order_disapproved_notification()  # TODO: DTO
        return order

    async def cancel_order(self, request: CancelOrderDTO) -> OrderOutputDTO:
        order = await self.cancel_order_use_case.execute(request)
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            await self.contractor_notification_service.send_order_cancelled_notification()  # TODO: DTO
        await self.contractee_notification_service.send_order_cancelled_notification()  # TODO: DTO
        return order

    async def close_order(self, request: CloseOrderDTO) -> OrderOutputDTO:
        order = await self.close_order_use_case.execute(request)
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            await self.contractor_notification_service.send_order_closed_notification()  # TODO: DTO
        return order

    async def open_order(self, request: OpenOrderDTO) -> OrderOutputDTO:
        order = await self.open_order_use_case.execute(request)
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            await self.contractor_notification_service.send_order_opened_notification()  # TODO: DTO
        return order

    async def fulfill_order(self, request: FulfillOrderDTO) -> OrderOutputDTO:
        order = await self.fulfill_order_use_case.execute(request)
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            await self.contractor_notification_service.send_order_fulfilled_notification()  # TODO: DTO
        await self.contractee_notification_service.send_order_fulfilled_notification()  # TODO: DTO
        return order


class AdminOrderQueryServiceImpl(
    AdminOrderQueryService, BaseOrderQueryService
):
    def __init__(
        self,
        get_order_use_case: GetOrderForAdminUseCase,
        get_orders_use_case: ListSupervisedOrdersUseCase,
        get_unassigned_order_use_case: GetUnassignedOrderUseCase,
    ):
        super().__init__(get_order_use_case, get_orders_use_case)
        self.get_unassigned_order_use_case = get_unassigned_order_use_case

    async def get_unassigned_order(
        self, query: LastObjectDTO
    ) -> CompleteOrderOutputDTO | None:
        return await self.get_unassigned_order_use_case.execute(query)

    async def get_user_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderOutputDTO]:
        # TODO: Добавить Use Case
        pass
