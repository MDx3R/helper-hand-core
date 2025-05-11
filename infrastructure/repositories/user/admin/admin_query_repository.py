from dataclasses import dataclass
from typing import List, Optional

from sqlalchemy import Select, select

from domain.dto.user.internal.user_filter_dto import (
    AdminFilterDTO,
)
from domain.entities.user.admin.admin import Admin
from domain.entities.user.admin.composite_admin import CompleteAdmin
from domain.repositories.user.admin.admin_query_repository import (
    AdminQueryRepository,
)
from infrastructure.database.mappers import AdminMapper
from infrastructure.database.models import (
    AdminBase,
    TelegramCredentialsBase,
    UserBase,
    WebCredentialsBase,
)
from infrastructure.repositories.base import QueryExecutor
from infrastructure.repositories.user.base import (
    UserQueryBuilder,
    build_statement_from_admin_filter,
    get_safe_attr,
    join_admin,
)


@dataclass
class UnmapperAdmin:
    user: UserBase
    admin: AdminBase
    web: Optional[WebCredentialsBase]
    telegram: Optional[TelegramCredentialsBase]


class AdminQueryRepositoryImpl(AdminQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_admin(self, user_id: int) -> Admin | None:
        query_builder = UserQueryBuilder()
        stmt = query_builder.add_admin().where_user_id(user_id).build()

        unmapped_admin = await self._execute_one(stmt)
        if not unmapped_admin:
            return None

        return AdminMapper.to_model(unmapped_admin.user, unmapped_admin.admin)

    async def get_complete_admin(self, user_id: int) -> CompleteAdmin | None:
        query_builder = UserQueryBuilder()
        stmt = (
            query_builder.add_admin()
            .add_credentials()
            .where_user_id(user_id)
            .build()
        )

        unmapped_admin = await self._execute_one(stmt)
        return  # TODO: Mapper

    async def filter_admins(self, query: AdminFilterDTO) -> List[Admin]:
        query_builder = UserQueryBuilder()
        stmt = query_builder.add_admin().apply_admin_filter(query).build()

        users = await self.executor.execute_many(stmt)
        return [AdminMapper.to_model(user, role) for user, role in users]

    async def _execute_one(self, statement: Select) -> UnmapperAdmin | None:
        row = await self.executor.execute_one(statement)
        if not row:
            return None

        return UnmapperAdmin(
            user=get_safe_attr(row, UserBase),
            admin=get_safe_attr(row, AdminBase),
            web=get_safe_attr(row, WebCredentialsBase),
            telegram=get_safe_attr(row, TelegramCredentialsBase),
        )
