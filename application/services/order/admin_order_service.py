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
    ListUnassignedOrdersUseCase,
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
    SetActiveOrderUseCase,
)
from domain.dto.base import LastObjectDTO
from domain.dto.order.internal.order_managment_dto import (
    ApproveOrderDTO,
    CancelOrderDTO,
    CloseOrderDTO,
    DisapproveOrderDTO,
    FulfillOrderDTO,
    OpenOrderDTO,
    SetOrderActiveDTO,
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
        set_order_active_use_case: SetActiveOrderUseCase,
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
        self.set_order_active_use_case = set_order_active_use_case
        self.fulfill_order_use_case = fulfill_order_use_case

        self.contractee_notification_service = contractee_notification_service
        self.contractor_notification_service = contractor_notification_service

    async def create_order(
        self, request: CreateOrderDTO
    ) -> OrderWithDetailsOutputDTO:
        order = await self.create_order_use_case.execute(request)
        # await self.contractee_notification_service.send_new_order_notification()  # TODO: DTO
        return order

    async def take_order(self, request: TakeOrderDTO) -> OrderOutputDTO:
        order = await self.take_order_use_case.execute(request)
        # Проверка на владение заказа не имеет смысла, так как подразумевается,
        # что заказ, созданный админом, не может быть заново подтвежден
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            ...
            # await self.contractor_notification_service.send_admin_assigned_notification()  # TODO: DTO
        return order

    async def approve_order(self, request: ApproveOrderDTO) -> OrderOutputDTO:
        order = await self.approve_order_use_case.execute(request)
        # Проверка на владение заказа не имеет смысла, так как подразумевается,
        # что заказ, созданный админом, не может быть заново подтвежден
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            ...
            # await self.contractor_notification_service.send_order_approved_notification()  # TODO: DTO
        return order

    async def disapprove_order(
        self, request: DisapproveOrderDTO
    ) -> OrderOutputDTO:
        order = await self.disapprove_order_use_case.execute(request)
        # Проверка на владение заказа не имеет смысла, так как подразумевается,
        # что заказ, созданный админом, не может быть заново подтвежден
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            ...
            # await self.contractor_notification_service.send_order_disapproved_notification()  # TODO: DTO
        return order

    async def cancel_order(self, request: CancelOrderDTO) -> OrderOutputDTO:
        order = await self.cancel_order_use_case.execute(request)
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            ...
            # await self.contractor_notification_service.send_order_cancelled_notification()  # TODO: DTO
        # await self.contractee_notification_service.send_order_cancelled_notification()  # TODO: DTO
        return order

    async def close_order(self, request: CloseOrderDTO) -> OrderOutputDTO:
        order = await self.close_order_use_case.execute(request)
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            ...
            # await self.contractor_notification_service.send_order_closed_notification()  # TODO: DTO
        return order

    async def open_order(self, request: OpenOrderDTO) -> OrderOutputDTO:
        order = await self.open_order_use_case.execute(request)
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            ...
            # await self.contractor_notification_service.send_order_opened_notification()  # TODO: DTO
        return order

    async def set_order_active(
        self, request: SetOrderActiveDTO
    ) -> OrderOutputDTO:
        # TODO: Уведомления
        return await self.set_order_active_use_case.execute(request)

    async def fulfill_order(self, request: FulfillOrderDTO) -> OrderOutputDTO:
        order = await self.fulfill_order_use_case.execute(request)
        if not OrderDomainService.is_owned_by(order, request.context.user_id):
            ...
            # await self.contractor_notification_service.send_order_fulfilled_notification()  # TODO: DTO
        # await self.contractee_notification_service.send_order_fulfilled_notification()  # TODO: DTO
        return order


class AdminOrderQueryServiceImpl(
    BaseOrderQueryService, AdminOrderQueryService
):
    def __init__(
        self,
        get_order_use_case: GetOrderForAdminUseCase,
        get_orders_use_case: ListSupervisedOrdersUseCase,
        list_unassigned_orders_use_case: ListUnassignedOrdersUseCase,
    ):
        super().__init__(get_order_use_case, get_orders_use_case)
        self.list_unassigned_orders_use_case = list_unassigned_orders_use_case

    async def get_unassigned_orders(
        self, query: PaginatedDTO
    ) -> List[OrderOutputDTO]:
        return await self.list_unassigned_orders_use_case.execute(query)

    async def get_user_orders(
        self, query: GetUserOrdersDTO
    ) -> List[OrderOutputDTO]:
        # TODO: Добавить Use Case
        return []
