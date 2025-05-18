from typing import Callable, Optional
from fastapi import Depends, HTTPException, Request, status
from dependency_injector.wiring import Provide, inject
from fastapi.security import OAuth2PasswordBearer

from application.services.auth.user_auth_service import (
    CredentialsExpiredException,
    InvalidCredentialsException,
    TokenService,
)
from core.containers import Container
from domain.dto.token import TokenClaims
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.entities.user.enums import RoleEnum
from domain.services.domain.services import UserDomainService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme_no_error = OAuth2PasswordBearer(
    tokenUrl="token", auto_error=False
)
auth_required = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Authentication required",
    headers={"WWW-Authenticate": "Bearer"},
)


def build_token_exception(exc: Exception) -> HTTPException:
    # TODO: В middleware?
    if isinstance(exc, CredentialsExpiredException):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if isinstance(exc, InvalidCredentialsException):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Internal server error: {exc}",
    )


@inject
async def get_claims_from_token(
    token: str = Depends(oauth2_scheme),
    service: TokenService = Depends(Provide[Container.token_service]),
) -> TokenClaims:
    try:
        return await service.extract_claims(token)
    except Exception as e:
        raise build_token_exception(e)


def get_current_user(request: Request) -> UserContextDTO:
    claims: TokenClaims = request.state.claims
    if not claims:
        raise auth_required
    return claims.user


def get_current_user_from_access_token(
    request: Request,
) -> UserContextDTO:
    claims: TokenClaims = request.state.claims
    if not claims or not claims.is_access:
        raise auth_required
    return claims.user


def has_role(
    *allowed_roles: RoleEnum,
) -> Callable:
    def checker(
        user: Optional[UserContextDTO] = Depends(
            get_current_user_from_access_token
        ),
    ) -> bool:
        return bool(user and UserDomainService.has_role(user, *allowed_roles))

    return checker


def is_guest(
    request: Request,
) -> bool:
    return not bool(request.state.claims)


def require_guest(request: Request) -> bool:
    if not is_guest(request):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are already logged in",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


def require_roles(*allowed_roles: RoleEnum) -> Callable:
    def checker(
        user: Optional[UserContextDTO] = Depends(
            get_current_user_from_access_token
        ),
    ) -> UserContextDTO:
        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not UserDomainService.has_role(user, *allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You lack the required permissions for this action",
            )
        return user

    return checker


authenticated = get_current_user
unauthenticated = require_guest
is_admin = has_role(RoleEnum.admin)
is_contractee = has_role(RoleEnum.contractee)
is_contractor = has_role(RoleEnum.contractor)
require_admin = require_roles(RoleEnum.admin)
require_contractee = require_roles(RoleEnum.contractee)
require_contractor = require_roles(RoleEnum.contractor)
