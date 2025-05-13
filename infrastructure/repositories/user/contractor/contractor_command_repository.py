from sqlalchemy import update
from domain.repositories.user.contractor.contractor_command_repository import (
    ContractorCommandRepository,
)
from infrastructure.database.mappers import ContractorMapper
from infrastructure.repositories.base import QueryExecutor

from domain.entities.user.contractor.contractor import Contractor
from infrastructure.database.models import ContractorBase, UserBase


class ContractorCommandRepositoryImpl(ContractorCommandRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def create_contractor(self, contractor: Contractor) -> Contractor:
        async with self.executor.transaction_manager.get_session() as session:
            user_base = ContractorMapper.to_user_base(contractor)
            self.executor.add(user_base)
            contractor_base = ContractorMapper.to_role_base(contractor)
            contractor_base.contractor_id = user_base.user_id
            self.executor.add(contractor_base)
        return ContractorMapper.to_model(user_base, contractor_base)

    async def update_contractor(self, contractor: Contractor) -> Contractor:
        stmt = (
            update(UserBase)
            .where(UserBase.user_id == contractor.user_id)
            .values(
                ContractorMapper.to_user_base(contractor).get_fields(),
            )
        )
        await self.executor.execute(stmt)
        stmt = (
            update(ContractorBase)
            .where(ContractorBase.contractor_id == contractor.contractor_id)
            .values(
                ContractorMapper.to_role_base(contractor).get_fields(),
            )
        )
        await self.executor.execute(stmt)
        return contractor
