from sqlalchemy import update
from domain.dto.user.internal.user_command_dto import SetUserStatusDTO
from domain.entities.user.credentials import (
    TelegramCredentials,
    WebCredentials,
)
from domain.entities.user.user import User
from infrastructure.database.models import (
    UserBase,
    TelegramCredentialsBase,
    WebCredentialsBase,
)
from domain.repositories.user.user_command_repository import (
    UserCommandRepository,
)
from infrastructure.repositories.base import QueryExecutor


class UserCommandRepositoryImpl(UserCommandRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def set_user_status(self, query: SetUserStatusDTO) -> None:
        stmt = (
            update(UserBase)
            .where(UserBase.user_id == query.user_id)
            .values(status=query.status)
        )
        await self.executor.execute(stmt)

    async def create_telegram_user(
        self, user: TelegramCredentials
    ) -> TelegramCredentials:
        telegram_user = TelegramCredentialsBase(
            telegram_id=user.telegram_id,
            chat_id=user.chat_id,
        )
        self.executor.add(telegram_user)
        return  # TODO: Mapper

    async def create_web_user(self, user: WebCredentials) -> WebCredentials:
        web_user = WebCredentialsBase(email=user.email, password=user.password)
        self.executor.add(web_user)
        return  # TODO: Mapper

    async def update_user(self, user: User) -> User:
        stmt = (
            update(UserBase)
            .where(UserBase.user_id == user.user_id)
            .values(
                surname=user.surname,
                name=user.name,
                patronymic=user.patronymic,
                phone_number=user.phone_number,
                role=user.role,
                status=user.status,
                photos=user.photos,
            )
        )
        await self.executor.execute(stmt)
        return user
