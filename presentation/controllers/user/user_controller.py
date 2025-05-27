from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from application.usecases.user.user_query_use_case import (
    GetProfileForUserUseCase,
)
from core.containers import Container
from dependency_injector.wiring import Provide, inject
from domain.dto.base import PaginationDTO
from domain.dto.user.internal.user_context_dto import (
    PaginatedDTO,
    UserContextDTO,
)
from domain.dto.user.internal.user_managment_dto import (
    ApproveUserDTO,
    DisapproveUserDTO,
)
from domain.dto.user.internal.user_query_dto import GetUserDTO
from domain.dto.user.response.admin.admin_output_dto import (
    CompleteAdminOutputDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    CompleteContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    CompleteContractorOutputDTO,
)
from domain.dto.user.response.user_output_dto import UserOutputDTO
from domain.services.user.admin_user_service import (
    AdminUserManagementService,
    AdminUserQueryService,
)
from domain.services.user.contractee_user_service import (
    ContracteeUserQueryService,
)
from domain.services.user.contractor_user_service import (
    ContractorUserQueryService,
)
from fastapi_utils.cbv import cbv

from presentation.controllers.permissions import (
    authenticated,
    is_admin,
    is_contractee,
    is_contractor,
    require_admin,
    require_contractee,
    require_contractor,
)
from presentation.controllers.utils import or_404

# Общий роутер для пользователей
router = APIRouter()


@inject
def get_user_use_case_factory(
    use_case: GetProfileForUserUseCase = Depends(
        Provide[Container.get_profile_for_user_use_case]
    ),
):
    return use_case


@cbv(router)
class UserController:
    get_profile_use_case: GetProfileForUserUseCase = Depends(
        get_user_use_case_factory
    )

    @router.get(
        "/me",
        response_model=UserOutputDTO,
    )
    async def get_me(self, user: UserContextDTO = Depends(authenticated)):
        return await self.get_profile_use_case.execute(user)


# Контроллер для заказчиков (Contractee)
contractee_router = APIRouter(dependencies=[Depends(is_contractee)])


@inject
def contractee_user_query_service_factory(
    service: ContracteeUserQueryService = Depends(
        Provide[Container.contractee_user_query_service]
    ),
):
    return service


@cbv(contractee_router)
class ContracteeUserController:
    service: ContracteeUserQueryService = Depends(
        contractee_user_query_service_factory
    )

    @contractee_router.get(
        "/me",
        response_model=CompleteContracteeOutputDTO,
    )
    async def get_me(self, user: UserContextDTO = Depends(require_contractee)):
        return await self.service.get_profile(user)

    @contractee_router.get(
        "/{user_id}",
        # response_model=UserOutputDTO, # TODO: Правильный тип
    )
    async def get_user(
        self, user_id: int, user: UserContextDTO = Depends(require_contractee)
    ):
        return or_404(
            await self.service.get_user(
                GetUserDTO(user_id=user_id, context=user)
            )
        )


# Контроллер для исполнителей (Contractor)
contractor_router = APIRouter(dependencies=[Depends(is_contractor)])


@inject
def contractor_user_query_service_factory(
    service: ContractorUserQueryService = Depends(
        Provide[Container.contractor_user_query_service]
    ),
):
    return service


@cbv(contractor_router)
class ContractorUserController:
    service: ContractorUserQueryService = Depends(
        contractor_user_query_service_factory
    )

    @contractor_router.get(
        "/me",
        response_model=CompleteContractorOutputDTO,
    )
    async def get_me(self, user: UserContextDTO = Depends(require_contractor)):
        return await self.service.get_profile(user)

    @contractor_router.get(
        "/{user_id}",
        # response_model=UserOutputDTO, # TODO: Правильный тип
    )
    async def get_user(
        self, user_id: int, user: UserContextDTO = Depends(require_contractor)
    ):
        return or_404(
            await self.service.get_user(
                GetUserDTO(user_id=user_id, context=user)
            )
        )


# Контроллер для администраторов
admin_router = APIRouter(dependencies=[Depends(is_admin)])


@inject
def admin_user_query_service_factory(
    service: AdminUserQueryService = Depends(
        Provide[Container.admin_user_query_service]
    ),
):
    return service


@inject
def admin_user_managment_service_factory(
    service: AdminUserManagementService = Depends(
        Provide[Container.admin_user_managment_service]
    ),
):
    return service


@cbv(admin_router)
class AdminUserController:
    query_service: AdminUserQueryService = Depends(
        admin_user_query_service_factory
    )
    command_service: AdminUserManagementService = Depends(
        admin_user_query_service_factory
    )

    @admin_router.get(
        "/me",
        response_model=CompleteAdminOutputDTO,
    )
    async def get_me(self, user: UserContextDTO = Depends(require_admin)):
        return await self.query_service.get_profile(user)

    @admin_router.get(
        "/pending",
        response_model=List[UserOutputDTO],
    )
    async def list_pending_users(
        self,
        params: PaginationDTO = Depends(),
        user: UserContextDTO = Depends(require_admin),
    ):
        return await self.query_service.get_pending_users(
            PaginatedDTO(
                last_id=params.last_id, size=params.size, context=user
            )
        )

    @admin_router.get(
        "/{user_id}",
        # response_model=UserOutputDTO, # TODO: Правильный тип
    )
    async def get_user(
        self, user_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return or_404(
            await self.query_service.get_user(
                GetUserDTO(user_id=user_id, context=user)
            )
        )

    @admin_router.get(
        "/{user_id}/approve",
        response_model=UserOutputDTO,
    )
    async def approve_user(
        self, user_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.command_service.approve_user(
            ApproveUserDTO(user_id=user_id, context=user)
        )

    @admin_router.get(
        "/{user_id}/disapprove",
        response_model=UserOutputDTO,
    )
    async def disapprove_user(
        self, user_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.command_service.disapprove_user(
            DisapproveUserDTO(user_id=user_id, context=user)
        )
