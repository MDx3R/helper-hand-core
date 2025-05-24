from re import S
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_utils.cbv import cbv
from dependency_injector.wiring import Provide, inject
from core.containers import Container
from domain.dto.base import PaginationDTO
from domain.dto.reply.response.reply_output_dto import (
    CompleteReplyOutputDTO,
    ReplyOutputDTO,
)
from domain.dto.user.internal.user_context_dto import (
    PaginatedDTO,
    UserContextDTO,
)
from domain.dto.reply.internal.reply_query_dto import (
    GetOrderRepliesDTO,
    GetDetailRepliesDTO,
    GetReplyDTO,
    GetOrderReplyDTO,
)
from domain.dto.reply.internal.reply_managment_dto import (
    ApproveReplyDTO,
    DisapproveReplyDTO,
)
from domain.services.reply.contractor_reply_service import (
    ContractorReplyManagmentService,
    ContractorReplyQueryService,
)
from presentation.controllers.permissions import (
    require_contractor,
    is_contractor,
)
from presentation.controllers.utils import or_404

contractor_reply_router = APIRouter(dependencies=[Depends(is_contractor)])


@inject
def contractor_reply_query_service_factory(
    service: ContractorReplyQueryService = Depends(
        Provide[Container.contractor_reply_query_service]
    ),
):
    return service


@inject
def contractor_reply_managment_service_factory(
    service: ContractorReplyManagmentService = Depends(
        Provide[Container.contractor_reply_managment_service]
    ),
):
    return service


@cbv(contractor_reply_router)
class ContractorReplyController:
    query_service: ContractorReplyQueryService = Depends(
        contractor_reply_query_service_factory
    )
    command_service: ContractorReplyManagmentService = Depends(
        contractor_reply_managment_service_factory
    )

    @contractor_reply_router.get(
        "/order/{order_id}", response_model=List[CompleteReplyOutputDTO]
    )
    async def list_order_replies(
        self,
        order_id: int,
        params: PaginationDTO = Depends(),
        user: UserContextDTO = Depends(require_contractor),
    ):
        return await self.query_service.get_order_replies(
            GetOrderRepliesDTO(
                order_id=order_id,
                context=user,
                last_id=params.last_id,
                size=params.size,
            )
        )

    @contractor_reply_router.get(
        "/detail/{detail_id}", response_model=List[CompleteReplyOutputDTO]
    )
    async def list_detail_replies(
        self,
        detail_id: int,
        params: PaginationDTO = Depends(),
        user: UserContextDTO = Depends(require_contractor),
    ):
        return await self.query_service.get_detail_replies(
            GetDetailRepliesDTO(
                detail_id=detail_id,
                context=user,
                last_id=params.last_id,
                size=params.size,
            )
        )

    @contractor_reply_router.get(
        "/pending", response_model=List[CompleteReplyOutputDTO]
    )
    async def get_pending_replies(
        self,
        params: PaginationDTO = Depends(),
        user: UserContextDTO = Depends(require_contractor),
    ):
        return await self.query_service.get_pending_replies(
            PaginatedDTO(
                context=user,
                last_id=params.last_id,
                size=params.size,
            )
        )

    @contractor_reply_router.get(
        "/pending/{order_id}", response_model=List[CompleteReplyOutputDTO]
    )
    async def get_pending_replies_for_order(
        self,
        order_id: int,
        params: PaginationDTO = Depends(),
        user: UserContextDTO = Depends(require_contractor),
    ):
        return await self.query_service.get_pending_replies_for_order(
            GetOrderRepliesDTO(
                order_id=order_id,
                context=user,
                last_id=params.last_id,
                size=params.size,
            )
        )

    @contractor_reply_router.get(
        "/{detail_id}/{contractee_id}", response_model=CompleteReplyOutputDTO
    )
    async def get_reply(
        self,
        detail_id: int,
        contractee_id: int,
        user: UserContextDTO = Depends(require_contractor),
    ):
        return or_404(
            await self.query_service.get_reply(
                GetReplyDTO(
                    detail_id=detail_id,
                    contractee_id=contractee_id,
                    context=user,
                )
            )
        )

    @contractor_reply_router.post(
        "/{detail_id}/{contractee_id}/approve", response_model=ReplyOutputDTO
    )
    async def approve_reply(
        self,
        detail_id: int,
        contractee_id: int,
        user: UserContextDTO = Depends(require_contractor),
    ):
        return await self.command_service.approve_reply(
            ApproveReplyDTO(
                detail_id=detail_id, contractee_id=contractee_id, context=user
            )
        )

    @contractor_reply_router.post(
        "/{detail_id}/{contractee_id}/disapprove",
        response_model=ReplyOutputDTO,
    )
    async def disapprove_reply(
        self,
        detail_id: int,
        contractee_id: int,
        user: UserContextDTO = Depends(require_contractor),
    ):
        return await self.command_service.disapprove_reply(
            DisapproveReplyDTO(
                detail_id=detail_id, contractee_id=contractee_id, context=user
            )
        )
