from typing import List

from domain.dto.user.internal.user_filter_dto import UserFilterDTO
from domain.entities.user.user import User
from domain.repositories.user.user_query_repository import UserQueryRepository
from infrastructure.database.mappers import UserMapper
from infrastructure.repositories.base import QueryExecutor
from infrastructure.repositories.user.base import UserQueryBuilder


class UserQueryRepositoryImpl(UserQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_user(self, user_id: int) -> User | None:
        stmt = UserQueryBuilder().where_user_id(user_id).build()

        user = await self.executor.execute_scalar_one(stmt)
        if not user:
            return None
        return UserMapper.to_model(user)

    async def filter_users(self, query: UserFilterDTO) -> List[User]:
        stmt = UserQueryBuilder().apply_user_filter(query).build()

        users = await self.executor.execute_scalar_many(stmt)
        return [UserMapper.to_model(user) for user in users]

    async def exists_by_filter(self, query: UserFilterDTO) -> bool:
        stmt = UserQueryBuilder().apply_user_filter(query).build()
        return bool(await self.executor.execute_scalar_one(stmt))
