from typing import List

from sqlalchemy import select

from domain.dto.user.internal.user_filter_dto import UserFilterDTO
from domain.entities.user.context import UserContext
from domain.entities.user.credentials import WebCredentials
from domain.entities.user.user import User
from domain.repositories.user.user_query_repository import UserQueryRepository
from infrastructure.database.mappers import (
    UserCredentialsMapper,
    UserMapper,
    WebCredentialsMapper,
)
from infrastructure.database.models import (
    TelegramCredentialsBase,
    UserBase,
    WebCredentialsBase,
)
from infrastructure.repositories.base import QueryExecutor
from infrastructure.repositories.user.base import (
    UnmappedUser,
    UserQueryBuilder,
)


class UserQueryRepositoryImpl(UserQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_user(self, user_id: int) -> User | None:
        stmt = self._get_query_buider().where_user_id(user_id).build()

        user = await self.executor.execute_scalar_one(stmt)
        if not user:
            return None
        return UserMapper.to_model(user)

    async def filter_users(self, query: UserFilterDTO) -> List[User]:
        stmt = self._get_query_buider().apply_user_filter(query).build()

        users = await self.executor.execute_scalar_many(stmt)
        return [UserMapper.to_model(user) for user in users]

    async def exists_by_query(self, query: UserFilterDTO) -> bool:
        stmt = self._get_query_buider().apply_user_filter(query).build()
        return bool(await self.executor.execute_scalar_one(stmt))

    async def get_web_credentials_by_email(
        self, email: str
    ) -> WebCredentials | None:
        stmt = select(WebCredentialsBase).where(
            WebCredentialsBase.email == email
        )
        result = await self.executor.execute_scalar_one(stmt)
        if not result:
            return None
        return WebCredentialsMapper.to_model(result)

    async def get_user_context_by_email(
        self, email: str
    ) -> UserContext | None:
        stmt = (
            select(UserBase, WebCredentialsBase, TelegramCredentialsBase)
            .outerjoin(
                WebCredentialsBase,
                UserBase.user_id == WebCredentialsBase.user_id,
            )
            .outerjoin(
                TelegramCredentialsBase,
                UserBase.user_id == TelegramCredentialsBase.user_id,
            )
            .where(WebCredentialsBase.email == email)
        )
        result = await self.executor.execute_one(stmt)
        if not result:
            return None

        unmapped = UnmappedUser(result)
        user = unmapped.user
        return UserContext(
            user_id=user.user_id,
            role=user.role,
            status=user.status,
            credentials=UserCredentialsMapper.to_model(
                unmapped.web, unmapped.telegram
            ),
        )

    def _get_query_buider(self) -> UserQueryBuilder:
        return UserQueryBuilder()
