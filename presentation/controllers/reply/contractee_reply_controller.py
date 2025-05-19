from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_utils.cbv import cbv
from dependency_injector.wiring import Provide, inject
from core.containers import Container
from domain.dto.reply.request.create_reply_dto import CreateReplyDTO
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
    GetReplyDTO,
)
from domain.services.reply.contractee_reply_service import (
    ContracteeReplyManagmentService,
    ContracteeReplyQueryService,
)
from presentation.controllers.permissions import (
    require_contractee,
    is_contractee,
)
from presentation.controllers.utils import or_404

contractee_reply_router = APIRouter(dependencies=[Depends(is_contractee)])


@inject
def contractee_reply_query_service_factory(
    service: ContracteeReplyQueryService = Depends(
        Provide[Container.contractee_reply_query_service]
    ),
):
    return service


@inject
def contractee_reply_managment_service_factory(
    service: ContracteeReplyManagmentService = Depends(
        Provide[Container.contractee_reply_managment_service]
    ),
):
    return service


@cbv(contractee_reply_router)
class ContracteeReplyController:
    query_service: ContracteeReplyQueryService = Depends(
        contractee_reply_query_service_factory
    )
    command_service: ContracteeReplyManagmentService = Depends(
        contractee_reply_managment_service_factory
    )

    @contractee_reply_router.get("/", response_model=List[ReplyOutputDTO])
    async def list_replies(
        self,
        last_id: int = Query(None, ge=1),
        size: int = Query(None, gt=0),
        user: UserContextDTO = Depends(require_contractee),
    ):
        if not size and last_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Size is required when last_id is provided",
            )
        return await self.query_service.get_replies(
            PaginatedDTO(last_id=last_id, size=size, context=user)
        )

    @contractee_reply_router.get(
        "/order/{order_id}", response_model=List[ReplyOutputDTO]
    )
    async def list_order_replies(
        self,
        order_id: int,
        last_id: int = Query(None, ge=1),
        size: int = Query(None, gt=0),
        user: UserContextDTO = Depends(require_contractee),
    ):
        if not size and last_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Size is required when last_id is provided",
            )
        return await self.query_service.get_order_replies(
            GetOrderRepliesDTO(
                order_id=order_id, last_id=last_id, size=size, context=user
            )
        )

    @contractee_reply_router.get(
        "/future", response_model=List[ReplyOutputDTO]
    )
    async def list_future_replies(
        self,
        last_id: int = Query(None, ge=1),
        size: int = Query(None, gt=0),
        user: UserContextDTO = Depends(require_contractee),
    ):
        if not size and last_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Size is required when last_id is provided",
            )
        return await self.query_service.get_future_replies(
            PaginatedDTO(last_id=last_id, size=size, context=user)
        )

    @contractee_reply_router.get(
        "/{detail_id}", response_model=CompleteReplyOutputDTO
    )
    async def get_reply(
        self,
        detail_id: int,
        user: UserContextDTO = Depends(require_contractee),
    ):
        return or_404(
            await self.query_service.get_reply(
                GetReplyDTO(
                    detail_id=detail_id,
                    contractee_id=user.user_id,
                    context=user,
                )
            )
        )

    @contractee_reply_router.post(
        "/{detail_id}", response_model=ReplyOutputDTO
    )
    async def submit_reply(
        self,
        detail_id: int,
        user: UserContextDTO = Depends(require_contractee),
    ):
        return await self.command_service.submit_reply(
            CreateReplyDTO(detail_id=detail_id, context=user)
        )
