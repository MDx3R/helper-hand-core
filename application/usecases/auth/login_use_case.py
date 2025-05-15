from application.external.password_hasher import PasswordHasher
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.user_auth_dto import LoginUserDTO
from domain.dto.user.response.user_output_dto import AuthOutputDTO
from domain.exceptions.service.auth import InvalidCredentialsException
from domain.mappers.user_mappers import UserContextMapper
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
