from datetime import date, datetime, timedelta, timezone
from jose import ExpiredSignatureError, jwt, JWTError
from application.external.blacklist import TokenBlacklist
from application.transactions import transactional
from application.usecases.auth.login_use_case import LoginUseCase
from application.usecases.auth.register_user_use_case import (
    RegisterContracteeUseCase,
    RegisterContractorUseCase,
)
from core.config import AuthConfig
from domain.dto.token import TokenClaims, TokenSignature
from domain.dto.user.base import UserCredentialsDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.contractee.contractee_registration_dto import (
    RegisterContracteeDTO,
)
from domain.dto.user.request.contractor.contractor_registration_dto import (
    RegisterContractorDTO,
)
from domain.dto.user.request.user_auth_dto import LoginUserDTO
from domain.dto.user.response.contractee.contractee_output_dto import (
    ContracteeOutputDTO,
    ContracteeRegistationOutputDTO,
)
from domain.dto.user.response.contractor.contractor_output_dto import (
    ContractorOutputDTO,
    ContractorRegistationOutputDTO,
)
from domain.dto.user.response.user_output_dto import AuthOutputDTO
from domain.entities.enums import CitizenshipEnum, GenderEnum
from domain.entities.token.enums import TokenTypeEnum
from domain.entities.token.token import Token
from domain.entities.user.enums import RoleEnum, UserStatusEnum
from domain.repositories.token.token_command_repository import (
    TokenCommandRepository,
)
from domain.repositories.token.token_query_repository import (
    TokenQueryRepository,
)
from domain.services.auth.token_service import TokenService
from domain.services.auth.user_auth_service import (
    UserAuthService,
)


class CredentialsExpiredException(Exception):
    pass


class CredentialsRevokedException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class JWTTokenBlacklist(TokenBlacklist):
    # TODO: Redis
    def __init__(self):
        pass

    async def add(self, token: str, expires_at: float):
        pass

    async def contains(self, token: str) -> bool:
        return False


class JWTTokenService(TokenService):
    def __init__(
        self,
        query_repository: TokenQueryRepository,
        command_repository: TokenCommandRepository,
        black_list: TokenBlacklist,
        config: AuthConfig,
    ):
        self.query_repository = query_repository
        self.command_repository = command_repository
        self.black_list = black_list
        self.config = config

    @transactional
    async def generate_token(self, context: UserContextDTO) -> AuthOutputDTO:
        access_token = self._create_access_token(context)
        refresh_token = self._create_refresh_token(context)

        # TODO: Сохранять в БД/Redis
        await self.command_repository.create_token(access_token)
        await self.command_repository.create_token(refresh_token)

        return AuthOutputDTO(
            user_id=context.user_id,
            access_token=access_token.token,
            refresh_token=refresh_token.token,
        )

    async def refresh_token(self, token: str):
        # TODO: Проверка на существование
        await self.query_repository.get_token(TokenSignature(token=token))

        claims = self.extract_claims(token)
        if not claims.is_refresh:
            raise InvalidCredentialsException

        # TODO: Получать актуальный контекст?
        # Можно ревокать старый токен и при изменении контекста возвращать новый
        context = claims.user

        access_token = self._create_access_token(context)
        refresh_token = self._create_refresh_token(context)

        # TODO: Пересохранять в БД/Redis
        await self.command_repository.create_token(access_token)
        await self.command_repository.create_token(refresh_token)

        return AuthOutputDTO(
            user_id=context.user_id,
            access_token=access_token.token,
            refresh_token=refresh_token.token,
        )

    async def get_user_context(self, token: str) -> UserContextDTO:
        if await self.black_list.contains(token):
            raise CredentialsRevokedException

        claims = self.extract_claims(token)
        if not claims.is_access:
            raise InvalidCredentialsException

        return claims.user

    def extract_claims(self, token: str) -> TokenClaims:
        try:
            claims = jwt.decode(
                token,
                key=self.config.SECRET_KEY,
                algorithms=[self.config.ALGORITHM],
            )
            return TokenClaims.model_validate(claims)
        except ExpiredSignatureError as e:
            raise CredentialsExpiredException from e
        except JWTError as e:
            raise InvalidCredentialsException from e

    def _create_access_token(self, context: UserContextDTO) -> Token:
        claims = self._build_claims(
            context,
            TokenTypeEnum.access,
            self.config.ACCESS_TOKEN_EXPIRATION_TIME,
        )
        jwt = self._create_jwt_token(claims)
        return self._build_token(context, jwt, claims)

    def _create_refresh_token(self, context: UserContextDTO) -> Token:
        claims = self._build_claims(
            context,
            TokenTypeEnum.refresh,
            self.config.REFRESH_TOKEN_EXPIRATION_TIME,
        )
        jwt = self._create_jwt_token(claims)
        return self._build_token(context, jwt, claims)

    def _build_claims(
        self,
        user: UserContextDTO,
        type: TokenTypeEnum,
        expires_in: timedelta,
    ) -> TokenClaims:
        return TokenClaims(
            user=user,
            type=type,
            exp=self._get_expiration_date(expires_in),
        )

    def _build_token(
        self, user: UserContextDTO, token: str, claims: TokenClaims
    ) -> Token:
        return Token(
            user_id=user.user_id,
            token=token,
            type=claims.type,
            expires_at=claims.exp,
        )

    def _create_jwt_token(self, token: TokenClaims) -> str:
        to_encode = token.model_dump()
        to_encode.update({"sub": token.user.user_id})
        to_encode.update({"iat": self._get_now().timestamp()})
        return jwt.encode(
            token.model_dump(),
            self.config.SECRET_KEY,
            algorithm=self.config.ALGORITHM,
        )

    def _get_expiration_date(self, expiration_time: timedelta) -> datetime:
        return self._get_now() + expiration_time

    def _get_now(self) -> datetime:
        return datetime.now(timezone.utc)


class UserAuthServiceImpl(UserAuthService):
    def __init__(
        self,
        login_use_case: LoginUseCase,
        register_contractor_use_case: RegisterContractorUseCase,
        register_contractee_use_case: RegisterContracteeUseCase,
    ):
        self.login_use_case = login_use_case
        self.register_contractor_use_case = register_contractor_use_case
        self.register_contractee_use_case = register_contractee_use_case

    async def login(self, request: LoginUserDTO) -> AuthOutputDTO:  # TODO: DTO
        return await self.login_use_case.execute(request)

    async def register_contractor(
        self, request: RegisterContractorDTO
    ) -> ContractorRegistationOutputDTO:
        # TODO: Уведомления
        pass
        # return await self.register_contractor_use_case.execute(request)

    async def register_contractee(
        self, request: RegisterContracteeDTO
    ) -> ContracteeRegistationOutputDTO:
        # TODO: Уведомления
        pass
        # return await self.register_contractee_use_case.execute(request)


class MockUserAuthService(UserAuthService):
    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    async def login(self, request: LoginUserDTO) -> AuthOutputDTO:  # TODO: DTO
        return await self.token_service.generate_token(
            UserContextDTO(
                user_id=1,
                role=RoleEnum.admin,
                status=UserStatusEnum.registered,
                credentials=UserCredentialsDTO(),
            )
        )

    async def register_contractor(
        self, request: RegisterContractorDTO
    ) -> ContractorRegistationOutputDTO:
        return ContractorRegistationOutputDTO(
            token=AuthOutputDTO(
                user_id=1, access_token="access", refresh_token="refresh"
            ),
            user=ContractorOutputDTO(
                surname="123",
                name="123",
                user_id=1,
                photos=[],
                role=RoleEnum.contractor,
                status=UserStatusEnum.registered,
                phone_number="123",
                about="123",
            ),
        )

    async def register_contractee(
        self, request: RegisterContracteeDTO
    ) -> ContracteeRegistationOutputDTO:
        return ContracteeRegistationOutputDTO(
            token=AuthOutputDTO(
                user_id=1, access_token="access", refresh_token="refresh"
            ),
            user=ContracteeOutputDTO(
                surname="123",
                name="123",
                user_id=1,
                photos=[],
                role=RoleEnum.contractor,
                status=UserStatusEnum.registered,
                phone_number="123",
                birthday=date(2005, 6, 16),
                height=185,
                gender=GenderEnum.male,
                citizenship=CitizenshipEnum.russia,
                positions=[],
            ),
        )
