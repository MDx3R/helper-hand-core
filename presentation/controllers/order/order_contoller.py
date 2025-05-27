from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_utils.cbv import cbv

from dependency_injector.wiring import Provide, inject
from core.containers import Container
from domain.dto.base import LastObjectDTO, PaginationDTO
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
    GetOrderAfterDTO,
    GetOrderDTO,
)
from domain.dto.order.request.create_order_dto import CreateOrderDTO
from domain.dto.order.request.order_input_dto import OrderWithDetailsInputDTO
from domain.dto.order.response.order_output_dto import (
    CompleteOrderOutputDTO,
    OrderDetailOutputDTO,
    OrderOutputDTO,
    OrderWithDetailsOutputDTO,
)
from domain.dto.user.internal.user_context_dto import (
    PaginatedDTO,
    UserContextDTO,
)
from domain.services.order.admin_order_service import (
    AdminOrderManagementService,
    AdminOrderQueryService,
)
from domain.services.order.contractee_order_service import (
    ContracteeOrderQueryService,
)
from domain.services.order.contractor_order_service import (
    ContractorOrderManagementService,
    ContractorOrderQueryService,
)

from domain.services.order.order_service import OrderQueryService
from presentation.controllers.permissions import (
    is_guest,
    require_contractor,
    is_contractor,
    is_admin,
    require_admin,
    is_contractee,
    require_contractee,
)
from presentation.controllers.utils import or_404


guest_router = APIRouter(dependencies=[Depends(is_guest)])


@inject
def order_query_service_factory(
    service: OrderQueryService = Depends(
        Provide[Container.order_query_service]
    ),
):
    return service


@cbv(guest_router)
class GuestOrderController:
    service: OrderQueryService = Depends(order_query_service_factory)

    @guest_router.get("/", response_model=List[OrderOutputDTO])
    async def list_orders(
        self,
        params: PaginationDTO = Depends(),
    ):
        return await self.service.get_recent_orders(params)


contractor_router = APIRouter(dependencies=[Depends(is_contractor)])


@inject
def contractor_order_query_service_factory(
    service: ContractorOrderQueryService = Depends(
        Provide[Container.contractor_order_query_service]
    ),
):
    return service


@inject
def contractor_order_managment_service_factory(
    service: ContractorOrderManagementService = Depends(
        Provide[Container.contractor_order_managment_service]
    ),
):
    return service


@cbv(contractor_router)
class ContractorUserController:
    query_service: ContractorOrderQueryService = Depends(
        contractor_order_query_service_factory
    )
    command_service: ContractorOrderManagementService = Depends(
        contractor_order_managment_service_factory
    )

    @contractor_router.post("/", response_model=OrderWithDetailsOutputDTO)
    async def create_order(
        self,
        request: OrderWithDetailsInputDTO,
        user: UserContextDTO = Depends(require_contractor),
    ):
        return await self.command_service.create_order(
            CreateOrderDTO(
                order=request.order,
                details=request.details,
                context=user,
            )
        )

    @contractor_router.get("/", response_model=List[OrderOutputDTO])
    async def list_orders(
        self,
        params: PaginationDTO = Depends(),
        user: UserContextDTO = Depends(require_contractor),
    ):
        return await self.query_service.get_orders(
            PaginatedDTO(
                last_id=params.last_id,
                size=params.size,
                context=user,
            )
        )

    @contractor_router.get(
        "/{order_id}",
        response_model=CompleteOrderOutputDTO,
    )
    async def get_order(
        self, order_id: int, user: UserContextDTO = Depends(require_contractor)
    ):
        return or_404(
            await self.query_service.get_order(
                GetOrderDTO(order_id=order_id, context=user)
            )
        )

    @contractor_router.post(
        "/{order_id}/cancel",
        response_model=OrderOutputDTO,
    )
    async def cancel_order(
        self, order_id: int, user: UserContextDTO = Depends(require_contractor)
    ):
        return await self.command_service.cancel_order(
            CancelOrderDTO(order_id=order_id, context=user)
        )

    @contractor_router.post(
        "/{order_id}/set-active",
        response_model=OrderOutputDTO,
    )
    async def set_active(
        self, order_id: int, user: UserContextDTO = Depends(require_contractor)
    ):
        return await self.command_service.set_order_active(
            SetOrderActiveDTO(order_id=order_id, context=user)
        )


contractee_router = APIRouter(dependencies=[Depends(is_contractee)])


@inject
def contractee_order_query_service_factory(
    service: ContracteeOrderQueryService = Depends(
        Provide[Container.contractee_order_query_service]
    ),
):
    return service


@cbv(contractee_router)
class ContracteeUserController:
    service: ContracteeOrderQueryService = Depends(
        contractee_order_query_service_factory
    )

    @contractee_router.get("/", response_model=List[OrderOutputDTO])
    async def list_orders(
        self,
        params: PaginationDTO = Depends(),
        user: UserContextDTO = Depends(require_contractee),
    ):
        return await self.service.get_orders(
            PaginatedDTO(
                last_id=params.last_id,
                size=params.size,
                context=user,
            )
        )

    @contractee_router.get(
        "/suitable",
        response_model=List[OrderWithDetailsOutputDTO],
    )
    async def get_suitable_orders(
        self,
        params: PaginationDTO = Depends(),
        user: UserContextDTO = Depends(require_contractee),
    ):
        return await self.service.get_suitable_orders(
            PaginatedDTO(
                last_id=params.last_id,
                size=params.size,
                context=user,
            )
        )

    @contractee_router.get(
        "/suitable/{order_id}",
        response_model=List[OrderDetailOutputDTO],
    )
    async def get_suitable_details_for_order(
        self,
        order_id: int,
        user: UserContextDTO = Depends(require_contractee),
    ):
        return await self.service.get_suitable_details_for_order(
            GetOrderDTO(order_id=order_id, context=user)
        )

    @contractee_router.get(
        "/{order_id}",
        response_model=CompleteOrderOutputDTO,
    )
    async def get_order(
        self, order_id: int, user: UserContextDTO = Depends(require_contractee)
    ):
        return or_404(
            await self.service.get_order(
                GetOrderDTO(order_id=order_id, context=user)
            )
        )


admin_router = APIRouter(dependencies=[Depends(is_admin)])


@inject
def admin_order_query_service_factory(
    service: AdminOrderQueryService = Depends(
        Provide[Container.admin_order_query_service]
    ),
):
    return service


@inject
def admin_order_managment_service_factory(
    service: AdminOrderManagementService = Depends(
        Provide[Container.admin_order_managment_service]
    ),
):
    return service


@cbv(admin_router)
class AdminUserController:
    query_service: AdminOrderQueryService = Depends(
        admin_order_query_service_factory
    )
    command_service: AdminOrderManagementService = Depends(
        admin_order_managment_service_factory
    )

    @admin_router.post("/", response_model=OrderWithDetailsOutputDTO)
    async def create_order(
        self,
        request: OrderWithDetailsInputDTO,
        user: UserContextDTO = Depends(require_admin),
    ):
        return await self.command_service.create_order(
            CreateOrderDTO(
                order=request.order,
                details=request.details,
                context=user,
            )
        )

    @admin_router.get("/", response_model=List[OrderOutputDTO])
    async def list_orders(
        self,
        params: PaginationDTO = Depends(),
        user: UserContextDTO = Depends(require_admin),
    ):
        return await self.query_service.get_orders(
            PaginatedDTO(
                last_id=params.last_id,
                size=params.size,
                context=user,
            )
        )

    @admin_router.get(
        "/pending",
        response_model=List[OrderOutputDTO],
    )
    async def list_pending_orders(
        self,
        params: PaginationDTO = Depends(),
        user: UserContextDTO = Depends(require_admin),
    ):
        return await self.query_service.get_unassigned_orders(
            PaginatedDTO(
                last_id=params.last_id,
                size=params.size,
                context=user,
            )
        )

    @admin_router.get(
        "/{order_id}",
        response_model=CompleteOrderOutputDTO,
    )
    async def get_order(
        self, order_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return or_404(
            await self.query_service.get_order(
                GetOrderDTO(order_id=order_id, context=user)
            )
        )

    @admin_router.post(
        "/{order_id}/take",
        response_model=OrderOutputDTO,
    )
    async def take_order(
        self, order_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.command_service.take_order(
            TakeOrderDTO(order_id=order_id, context=user)
        )

    @admin_router.post(
        "/{order_id}/approve",
        response_model=OrderOutputDTO,
    )
    async def approve_order(
        self, order_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.command_service.approve_order(
            ApproveOrderDTO(order_id=order_id, context=user)
        )

    @admin_router.post(
        "/{order_id}/disapprove",
        response_model=OrderOutputDTO,
    )
    async def disapprove_order(
        self, order_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.command_service.disapprove_order(
            DisapproveOrderDTO(order_id=order_id, context=user)
        )

    @admin_router.post(
        "/{order_id}/cancel",
        response_model=OrderOutputDTO,
    )
    async def cancel_order(
        self, order_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.command_service.cancel_order(
            CancelOrderDTO(order_id=order_id, context=user)
        )

    @admin_router.post(
        "/{order_id}/close",
        response_model=OrderOutputDTO,
    )
    async def close_order(
        self, order_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.command_service.close_order(
            CloseOrderDTO(order_id=order_id, context=user)
        )

    @admin_router.post(
        "/{order_id}/open",
        response_model=OrderOutputDTO,
    )
    async def open_order(
        self, order_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.command_service.open_order(
            OpenOrderDTO(order_id=order_id, context=user)
        )

    @admin_router.post(
        "/{order_id}/set-active",
        response_model=OrderOutputDTO,
    )
    async def set_active(
        self, order_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.command_service.set_order_active(
            SetOrderActiveDTO(order_id=order_id, context=user)
        )

    @admin_router.post(
        "/{order_id}/fulfill",
        response_model=OrderOutputDTO,
    )
    async def fulfill_order(
        self, order_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.command_service.fulfill_order(
            FulfillOrderDTO(order_id=order_id, context=user)
        )
