from fastapi import APIRouter, Depends
from core.containers import Container
from dependency_injector.wiring import Provide, inject
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.internal.user_query_dto import GetUserDTO
from domain.dto.user.response.admin.admin_output_dto import (
    AdminOutputDTO,
    CompleteAdminOutputDTO,
)
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
)
from domain.dto.user.response.user_output_dto import UserOutputDTO
from domain.entities.user.enums import RoleEnum, UserStatusEnum
from domain.services.user.admin_user_service import AdminUserQueryService
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

# Общий роутер для пользователей
router = APIRouter()


# @cbv(router)
# class UserController:
#     @router.get(
#         "/me",
#         response_model=UserOutputDTO,
#     )
#     async def get_me(self, user: UserContextDTO =Depends(authenticated)):
#         return UserOutputDTO(
#             surname="123",
#             name="123",
#             user_id=1,
#             photos=[],
#             role=RoleEnum.contractor,
#             status=UserStatusEnum.registered,
#             phone_number="123",
#         )


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
    @contractee_router.get(
        "/me",
        response_model=ContracteeOutputDTO,
    )
    async def get_me(self, user: UserContextDTO = Depends(require_contractee)):
        pass

    @contractee_router.get(
        "/{user_id}",
        response_model=UserOutputDTO,
    )
    async def get_user(
        self, user_id: int, user: UserContextDTO = Depends(require_contractee)
    ):
        pass


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
    @contractor_router.get(
        "/me",
        response_model=ContractorOutputDTO,
    )
    async def get_me(self, user: UserContextDTO = Depends(require_contractor)):
        pass

    @contractor_router.get(
        "/{user_id}",
        response_model=UserOutputDTO,
    )
    async def get_user(
        self, user_id: int, user: UserContextDTO = Depends(require_contractor)
    ):
        pass


# Контроллер для администраторов
admin_router = APIRouter(dependencies=[Depends(is_admin)])


@inject
def admin_user_query_service_factory(
    service: AdminUserQueryService = Depends(
        Provide[Container.admin_user_query_service]
    ),
):
    return service


@cbv(admin_router)
class AdminUserController:
    service: AdminUserQueryService = Depends(admin_user_query_service_factory)

    @admin_router.get(
        "/me",
        response_model=CompleteAdminOutputDTO,
    )
    async def get_me(self, user: UserContextDTO = Depends(require_admin)):
        return await self.service.get_profile(user)

    @admin_router.get(
        "/pending",
        # response_model=UserOutputDTO, # TODO: Правильный тип
    )
    async def get_pending_user(self):
        return await self.service.get_pending_user()

    @admin_router.get(
        "/{user_id}",
        # response_model=UserOutputDTO, # TODO: Правильный тип
    )
    async def get_user(
        self, user_id: int, user: UserContextDTO = Depends(require_admin)
    ):
        return await self.service.get_user(
            GetUserDTO(user_id=user_id, context=user)
        )
