from sqlalchemy import update
from domain.dto.user.internal.user_command_dto import SetUserStatusDTO
from domain.entities.user.credentials import (
    TelegramCredentials,
    WebCredentials,
)
from domain.entities.user.user import User
from domain.exceptions.service.common import NotFoundException
from infrastructure.database.mappers import (
    TelegramCredentialsMapper,
    UserMapper,
    WebCredentialsMapper,
)
from infrastructure.database.models import (
    UserBase,
)
from domain.repositories.user.user_command_repository import (
    UserCommandRepository,
)
from infrastructure.repositories.base import QueryExecutor


class UserCommandRepositoryImpl(UserCommandRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def set_user_status(self, query: SetUserStatusDTO) -> User:
        stmt = (
            update(UserBase)
            .where(UserBase.user_id == query.user_id)
            .values(status=query.status)
            .returning(UserBase)
        )
        user = await self.executor.execute_scalar_one(stmt)
        if not user:
            raise NotFoundException()
        return UserMapper.to_model(user)

    async def create_telegram_user(
        self, user: TelegramCredentials
    ) -> TelegramCredentials:
        base = TelegramCredentialsMapper.to_base(user)
        await self.executor.add(base)
        return TelegramCredentialsMapper.to_model(base)

    async def create_web_user(self, user: WebCredentials) -> WebCredentials:
        base = WebCredentialsMapper.to_base(user)
        await self.executor.add(base)
        return WebCredentialsMapper.to_model(base)

    async def update_user(self, user: User) -> User:
        stmt = (
            update(UserBase)
            .where(UserBase.user_id == user.user_id)
            .values(user.get_fields())
        )
        await self.executor.execute(stmt)
        return user
