from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import Provide, inject
from core.containers import Container
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.contractee.contractee_registration_dto import (
    RegisterContracteeDTO,
)
from domain.dto.user.request.contractor.contractor_registration_dto import (
    RegisterContractorDTO,
)
from domain.dto.user.request.user_auth_dto import LoginUserDTO
from domain.dto.user.response.user_output_dto import AuthOutputDTO
from domain.services.auth.token_service import TokenService
from domain.services.auth.user_auth_service import UserAuthService

from fastapi_utils.cbv import cbv

from presentation.controllers.permissions import (
    build_token_exception,
    authenticated,
    oauth2_scheme,
    require_guest,
)


@inject
def token_service_factory(
    service: TokenService = Depends(Provide[Container.token_service]),
):
    return service


@inject
def auth_service_factory(
    service: UserAuthService = Depends(Provide[Container.auth_service]),
):
    return service


router = APIRouter()


@router.get("/")
def hello(user: UserContextDTO = Depends(authenticated)):
    return f"Hello, {user.user_id}"


@cbv(router)
class AuthController:
    token_service: TokenService = Depends(token_service_factory)
    auth_service: UserAuthService = Depends(auth_service_factory)

    @router.post(
        "/login",
        response_model=AuthOutputDTO,
        dependencies=[Depends(require_guest)],
    )
    async def login(
        self,
        form_data: OAuth2PasswordRequestForm = Depends(),
    ):
        return await self.auth_service.login(
            LoginUserDTO(email=form_data.username, password=form_data.password)
        )

    @router.post("/register/contractee", dependencies=[Depends(require_guest)])
    async def register_contractee(
        self,
        request: RegisterContracteeDTO,
    ):
        return await self.auth_service.register_contractee(request)

    @router.post("/register/contractor", dependencies=[Depends(require_guest)])
    async def register_contractor(
        self,
        request: RegisterContractorDTO,
    ):
        return await self.auth_service.register_contractor(request)

    @router.post("/refresh")
    async def refresh(
        self,
        token: str = Depends(oauth2_scheme),
    ):
        try:
            return await self.token_service.refresh_token(token)
        except Exception as e:  # TODO: В middleware?
            raise build_token_exception(e)
