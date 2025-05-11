from infrastructure.repositories.user.base import (
    UserQueryBuilder,
    get_safe_attr,
)
from domain.dto.user.internal.user_filter_dto import ContracteeFilterDTO
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractee.composite_contractee import (
    CompleteContractee,
)
from domain.repositories.user.contractee.contractee_query_repository import (
    ContracteeQueryRepository,
)
from infrastructure.database.mappers import ContracteeMapper
from infrastructure.repositories.base import QueryExecutor
from typing import List
from dataclasses import dataclass
from typing import Optional
from infrastructure.database.models import (
    UserBase,
    ContracteeBase,
    WebCredentialsBase,
    TelegramCredentialsBase,
)


@dataclass
class UnmapperContractee:
    user: UserBase
    contractee: ContracteeBase
    web: Optional[WebCredentialsBase]
    telegram: Optional[TelegramCredentialsBase]


class ContracteeQueryRepositoryImpl(ContracteeQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_contractee(self, user_id: int) -> Contractee | None:
        query_builder = UserQueryBuilder()
        stmt = query_builder.add_contractee().where_user_id(user_id).build()

        unmapped_contractee = await self._execute_one(stmt)
        if not unmapped_contractee:
            return None

        return ContracteeMapper.to_model(
            unmapped_contractee.user, unmapped_contractee.contractee
        )

    async def get_complete_contractee(
        self, user_id: int
    ) -> CompleteContractee | None:
        query_builder = UserQueryBuilder()
        stmt = (
            query_builder.add_contractee()
            .add_credentials()
            .where_user_id(user_id)
            .build()
        )

        unmapped_contractee = await self._execute_one(stmt)
        return  # TODO: Mapper

    async def filter_contractees(
        self, query: ContracteeFilterDTO
    ) -> List[Contractee]:
        query_builder = UserQueryBuilder()
        stmt = (
            query_builder.add_contractee()
            .apply_contractee_filter(query)
            .build()
        )

        users = await self.executor.execute_many(stmt)
        return [ContracteeMapper.to_model(user, role) for user, role in users]

    async def _execute_one(self, statement):
        row = await self.executor.execute_one(statement)
        if not row:
            return None

        return UnmapperContractee(
            user=get_safe_attr(row, UserBase),
            contractee=get_safe_attr(row, ContracteeBase),
            web=get_safe_attr(row, WebCredentialsBase),
            telegram=get_safe_attr(row, TelegramCredentialsBase),
        )
