from typing import List

from sqlalchemy import Select, select

from domain.dto.user.internal.user_filter_dto import UserFilterDTO
from domain.entities.user.user import User
from domain.repositories.user.user_query_repository import UserQueryRepository
from infrastructure.database.mappers import UserMapper
from infrastructure.database.models import UserBase
from infrastructure.repositories.base import O, QueryExecutor


class UserQueryRepositoryImpl(UserQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_user(self, user_id: int) -> User | None:
        stmt = select(UserBase).where(UserBase.user_id == user_id)

        user = await self.executor.execute_scalar_one(stmt)
        return UserMapper.to_model(user)

    async def filter_users(self, query: UserFilterDTO) -> List[User]:
        stmt = self._build_statement_from_filter(select(UserBase), query)

        users = await self.executor.execute_scalar_many(stmt)
        return [UserMapper.to_model(user) for user in users]

    async def exists_by_filter(self, query: UserFilterDTO) -> bool:
        stmt = self._build_statement_from_filter(select(1), query)
        return bool(await self.executor.execute_scalar_one(stmt))

    def _build_statement_from_filter(
        self, stmt: Select[O], filter: UserFilterDTO
    ) -> Select[O]:
        if filter.status:
            stmt = stmt.where(UserBase.status == filter.status)
        if filter.phone_number:
            stmt = stmt.where(UserBase.phone_number == filter.phone_number)
        if filter.role:
            stmt = stmt.where(UserBase.role == filter.role)
        if filter.last_id:
            stmt = stmt.where(UserBase.user_id > filter.last_id)
        if filter.size:
            stmt = stmt.limit(filter.size)
        return stmt
