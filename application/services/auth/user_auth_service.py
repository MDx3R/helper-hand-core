from datetime import date, datetime, timedelta, timezone
from queue import Queue
from typing import Literal
from jose import ExpiredSignatureError, jwt, JWTError
from pydantic import BaseModel
from application.external.blacklist import TokenBlacklist
from core.config import AuthConfig
from domain.dto.token import TokenClaims
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
from domain.entities.user.enums import RoleEnum, UserStatusEnum
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

    def add(self, token: str, expires_at: float):
        pass

    def contains(self, token: str) -> bool:
        return False


class JWTTokenService(TokenService):
    def __init__(self, black_list: JWTTokenBlacklist, config: AuthConfig):
        self.black_list = black_list
        self.config = config

    async def generate_token(self, context: UserContextDTO) -> AuthOutputDTO:
        token = AuthOutputDTO(
            access_token=self._create_access_token(context),
            refresh_token=self._create_refresh_token(context),
        )
        # TODO: Сохранять в БД/Redis
        return token

    async def refresh_token(self, refresh_token: str):
        # TODO: Проверка на существование

        claims = self.extract_claims(refresh_token)
        if not claims.is_refresh:
            raise InvalidCredentialsException

        # TODO: Получать актуальный контекст?
        # Можно ревокать старый токен и при изменении контекста возвращать новый
        context = claims.user
        token = AuthOutputDTO(
            access_token=self._create_access_token(context),
            refresh_token=self._create_refresh_token(context),
        )
        # TODO: Пересохранять в БД/Redis
        return token

    def get_user_context(self, access_token: str) -> UserContextDTO:
        if self.black_list.contains(access_token):
            raise CredentialsRevokedException

        claims = self.extract_claims(access_token)
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

    def _create_access_token(self, context: UserContextDTO) -> str:
        token = self._build_token(
            context, "access", self.config.ACCESS_TOKEN_EXPIRATION_TIME
        )
        return self._create_jwt_token(token)

    def _create_refresh_token(self, context: UserContextDTO) -> str:
        token = self._build_token(
            context, "refresh", self.config.REFRESH_TOKEN_EXPIRATION_TIME
        )
        return self._create_jwt_token(token)

    def _build_token(
        self,
        user: UserContextDTO,
        type: Literal["access", "refresh"],
        expires_in: timedelta,
    ) -> TokenClaims:
        return TokenClaims(
            user=user,
            type=type,
            exp=self._get_expiration_date(expires_in),
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


class MockUserAuthService(UserAuthService):
    def __init__(self, token_service: TokenService):
        self.token_service = token_service

    async def login(self, request: LoginUserDTO) -> AuthOutputDTO:  # TODO: DTO
        return await self.token_service.generate_token(
            UserContextDTO(
                user_id=1,
                photos=[],
                role=RoleEnum.admin,
                status=UserStatusEnum.registered,
                credentials=UserCredentialsDTO(),
            )
        )
        return AuthOutputDTO(access_token="access", refresh_token="refresh")

    async def register_contractor(
        self, request: RegisterContractorDTO
    ) -> ContractorRegistationOutputDTO:
        return ContractorRegistationOutputDTO(
            token=AuthOutputDTO(
                access_token="access", refresh_token="refresh"
            ),
            contractor=ContractorOutputDTO(
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
                access_token="access", refresh_token="refresh"
            ),
            contractor=ContracteeOutputDTO(
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
