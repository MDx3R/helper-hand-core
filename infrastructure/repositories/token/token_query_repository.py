from typing import List

from sqlalchemy import Select, select

from domain.dto.token import TokenFilter, TokenSignature
from domain.entities.token.token import Token
from domain.repositories.token.token_query_repository import (
    TokenQueryRepository,
)
from domain.time import get_current_time
from infrastructure.database.mappers import TokenMapper
from infrastructure.database.models import TokenBase
from infrastructure.repositories.base import QueryExecutor


class TokenQueryRepositoryImpl(TokenQueryRepository):
    def __init__(self, executor: QueryExecutor) -> None:
        self.executor = executor

    async def get_token(self, signature: TokenSignature) -> Token | None:
        stmt = self.apply_signature(select(TokenBase), signature)

        result = await self.executor.execute_scalar_one(stmt)
        if not result:
            return None
        return TokenMapper.to_model(result)

    async def get_tokens(self, query: TokenFilter) -> List[Token]:
        stmt = self.apply_filter(select(TokenBase), query)

        results = await self.executor.execute_scalar_many(stmt)
        return [TokenMapper.to_model(token) for token in results]

    def apply_signature(
        self, stmt: Select, signature: TokenSignature
    ) -> Select:
        stmt = stmt.where(TokenBase.token == signature.token)
        stmt = self.apply_filter(stmt, signature)
        return stmt

    def apply_filter(self, stmt: Select, signature: TokenFilter) -> Select:
        if signature.user_id:
            stmt = stmt.where(TokenBase.user_id == signature.user_id)
        if signature.type:
            stmt = stmt.where(TokenBase.type == signature.type)
        if signature.revoked is not None:
            stmt = stmt.where(TokenBase.revoked == signature.revoked)
        if signature.expired is not None:
            if signature.expired:
                clause = TokenBase.expires_at < get_current_time()
            else:
                clause = TokenBase.expires_at > get_current_time()
            stmt = stmt.where(clause)

        return stmt
