from uuid import UUID
from application.external.blacklist import TokenBlacklist
from application.external.password_hasher import PasswordHasher
from domain.dto.token import TokenFilter, TokenSignature
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.user_auth_dto import LoginUserDTO
from domain.dto.user.response.user_output_dto import AuthOutputDTO
from domain.entities.token.enums import TokenTypeEnum
from domain.entities.token.token import Token
from domain.exceptions.service.auth import (
    InvalidCredentialsException,
    UnauthorizedAccessException,
)
from domain.mappers.user_mappers import UserContextMapper
from domain.repositories.token.token_command_repository import (
    TokenCommandRepository,
)
from domain.repositories.token.token_query_repository import (
    TokenQueryRepository,
)
from domain.repositories.user.user_query_repository import UserQueryRepository
from domain.services.auth.token_service import TokenService


class LoginUseCase:
    def __init__(
        self,
        token_service: TokenService,
        password_hasher: PasswordHasher,
        user_query_repository: UserQueryRepository,
    ) -> None:
        self.token_service = token_service
        self.password_hasher = password_hasher
        self.user_query_repository = user_query_repository

    async def execute(self, request: LoginUserDTO) -> AuthOutputDTO:
        context = await self.user_query_repository.get_user_context_by_email(
            request.email
        )
        if not context or not context.credentials.web:
            raise InvalidCredentialsException("Неверный логин")

        if not self.password_hasher.verify(
            request.password, context.credentials.web.password
        ):
            raise InvalidCredentialsException("Неверный пароль")

        return await self.token_service.generate_token(
            UserContextMapper.to_dto(context)
        )


class LogoutUseCase:
    def __init__(
        self,
        token_query_repository: TokenQueryRepository,
        token_command_repository: TokenCommandRepository,
        token_blacklist: TokenBlacklist,
        token_service: TokenService,
    ) -> None:
        self.token_query_repository = token_query_repository
        self.token_command_repository = token_command_repository
        self.token_service = token_service
        self.token_blacklist = token_blacklist

    async def execute(self, access_token: str) -> None:
        claims = await self.token_service.extract_claims(access_token)
        token_pair = (
            await self.token_query_repository.get_token_pair_by_session(
                claims.session
            )
        )
        if not token_pair:
            raise InvalidCredentialsException("Недействительный токен")

        await self.token_command_repository.revoke_tokens_by_session(
            claims.session
        )
        await self.blacklist_token(token_pair.access_token)
        await self.blacklist_token(token_pair.refresh_token)

    async def blacklist_token(self, token: Token):
        await self.token_blacklist.add(
            token.token,
            token.expires_at.timestamp(),
        )
