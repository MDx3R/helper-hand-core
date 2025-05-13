from infrastructure.repositories.user.base import (
    UnmappedUser,
    UserQueryBuilder,
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
from infrastructure.repositories.base import QueryExecutor, frozen
from typing import List
from infrastructure.database.models import ContracteeBase


@frozen(init=False)
class UnmappedContractee(UnmappedUser):
    contractee: ContracteeBase


class ContracteeQueryRepositoryImpl(ContracteeQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_contractee(self, user_id: int) -> Contractee | None:
        query_builder = self._get_query_buider()
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
        query_builder = self._get_query_buider()
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
        query_builder = self._get_query_buider()
        stmt = (
            query_builder.add_contractee()
            .apply_contractee_filter(query)
            .build()
        )

        users = await self.executor.execute_many(stmt)
        return [ContracteeMapper.to_model(user, role) for user, role in users]

    def _get_query_buider(self) -> UserQueryBuilder:
        return UserQueryBuilder()

    async def _execute_one(self, statement) -> UnmappedContractee | None:
        row = await self.executor.execute_one(statement)
        if not row:
            return None

        return UnmappedContractee(row)
