from dataclasses import asdict
from typing import List, Optional

from sqlalchemy import Select

from domain.dto.user.internal.user_filter_dto import (
    AdminFilterDTO,
)
from domain.entities.user.admin.admin import Admin
from domain.entities.user.admin.composite_admin import CompleteAdmin
from domain.entities.user.credentials import UserCredentials
from domain.repositories.user.admin.admin_query_repository import (
    AdminQueryRepository,
)
from infrastructure.database.mappers import (
    AdminMapper,
    CompleteAdminMapper,
    UserCredentialsMapper,
)
from infrastructure.database.models import (
    AdminBase,
    ContractorBase,
)
from infrastructure.repositories.base import (
    JoinType,
    QueryExecutor,
    frozen,
)
from infrastructure.repositories.user.base import (
    UnmappedUser,
    UserQueryBuilder,
)


@frozen(init=False)
class UnmappedAdmin(UnmappedUser):
    admin: AdminBase
    contractor: Optional[ContractorBase]


class AdminQueryRepositoryImpl(AdminQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_admin(self, user_id: int) -> Admin | None:
        query_builder = self._get_query()
        stmt = query_builder.where_user_id(user_id).build()

        unmapped = await self._execute_one(stmt)
        if not unmapped:
            return None

        return AdminMapper.to_model(unmapped.user, unmapped.admin)

    async def get_complete_admin(self, user_id: int) -> CompleteAdmin | None:
        query_builder = self._get_query()
        stmt = (
            query_builder.add_admin()
            .add_contractor(JoinType.OUTER)
            .add_credentials()
            .where_user_id(user_id)
            .build()
        )

        unmapped = await self._execute_one(stmt)
        if not unmapped:
            return None
        return CompleteAdminMapper.to_model(
            unmapped.user,
            unmapped.admin,
            unmapped.contractor,
            unmapped.web,
            unmapped.telegram,
        )

    async def filter_admins(self, query: AdminFilterDTO) -> List[Admin]:
        query_builder = self._get_query()
        stmt = query_builder.add_admin().apply_admin_filter(query).build()

        users = await self.executor.execute_many(stmt)
        return [AdminMapper.to_model(user, role) for user, role in users]

    def _get_query(self) -> UserQueryBuilder:
        return self._get_query_buider().add_admin()

    def _get_query_buider(self) -> UserQueryBuilder:
        return UserQueryBuilder()

    async def _execute_one(self, statement: Select) -> UnmappedAdmin | None:
        row = await self.executor.execute_one(statement)
        if not row:
            return None
        return UnmappedAdmin(row)
