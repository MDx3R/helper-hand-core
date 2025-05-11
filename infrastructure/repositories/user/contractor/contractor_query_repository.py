from infrastructure.repositories.user.base import (
    UserQueryBuilder,
    get_safe_attr,
)
from domain.dto.user.internal.user_filter_dto import ContractorFilterDTO
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.contractor.composite_contractor import (
    CompleteContractor,
)
from domain.repositories.user.contractor.contractor_query_repository import (
    ContractorQueryRepository,
)
from infrastructure.database.mappers import ContractorMapper
from infrastructure.repositories.base import QueryExecutor
from typing import List
from dataclasses import dataclass
from typing import Optional
from infrastructure.database.models import (
    UserBase,
    ContractorBase,
    WebCredentialsBase,
    TelegramCredentialsBase,
)


@dataclass
class UnmapperContractor:
    user: UserBase
    contractor: ContractorBase
    web: Optional[WebCredentialsBase]
    telegram: Optional[TelegramCredentialsBase]


class ContractorQueryRepositoryImpl(ContractorQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_contractor(self, user_id: int) -> Contractor | None:
        query_builder = UserQueryBuilder()
        stmt = query_builder.add_contractor().where_user_id(user_id).build()

        unmapped_contractor = await self._execute_one(stmt)
        if not unmapped_contractor:
            return None

        return ContractorMapper.to_model(
            unmapped_contractor.user, unmapped_contractor.contractor
        )

    async def get_complete_contractor(
        self, user_id: int
    ) -> CompleteContractor | None:
        query_builder = UserQueryBuilder()
        stmt = (
            query_builder.add_contractor()
            .add_credentials()
            .where_user_id(user_id)
            .build()
        )

        unmapped_contractor = await self._execute_one(stmt)
        return  # TODO: Mapper

    async def filter_contractors(
        self, query: ContractorFilterDTO
    ) -> List[Contractor]:
        query_builder = UserQueryBuilder()
        stmt = (
            query_builder.add_contractor()
            .apply_contractor_filter(query)
            .build()
        )

        users = await self.executor.execute_many(stmt)
        return [ContractorMapper.to_model(user, role) for user, role in users]

    async def _execute_one(self, statement):
        row = await self.executor.execute_one(statement)
        if not row:
            return None

        return UnmapperContractor(
            user=get_safe_attr(row, UserBase),
            contractor=get_safe_attr(row, ContractorBase),
            web=get_safe_attr(row, WebCredentialsBase),
            telegram=get_safe_attr(row, TelegramCredentialsBase),
        )
