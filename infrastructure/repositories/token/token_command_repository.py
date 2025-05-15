from sqlalchemy import update
from domain.entities.token.token import Token
from domain.exceptions.service.common import NotFoundException
from domain.repositories.token.token_command_repository import (
    TokenCommandRepository,
)
from infrastructure.database.mappers import TokenMapper
from infrastructure.database.models import TokenBase
from infrastructure.repositories.base import QueryExecutor


class TokenCommandRepositoryImpl(TokenCommandRepository):
    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def create_token(self, token: Token) -> Token:
        base = TokenMapper.to_base(token)
        await self.executor.add(base)
        return TokenMapper.to_model(base)

    async def revoke_token(self, token: str) -> Token:
        stmt = (
            update(TokenBase)
            .where(TokenBase.token == token)
            .values(revoked=True)
            .returning(TokenBase)
        )
        result = await self.executor.execute_scalar_one(stmt)
        if not result:
            raise NotFoundException()
        return TokenMapper.to_model(result)
