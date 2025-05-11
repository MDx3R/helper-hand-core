from sqlalchemy import update
from domain.repositories.user.contractor.contractor_command_repository import (
    ContractorCommandRepository,
)
from infrastructure.repositories.base import QueryExecutor

from domain.entities.user.contractor.contractor import Contractor
from infrastructure.database.models import ContractorBase


class ContractorCommandRepositoryImpl(ContractorCommandRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def create_contractor(self, contractor: Contractor) -> Contractor:
        contractor_base = ContractorBase(
            contractor_id=contractor.contractor_id,
            about=contractor.about,
        )
        self.executor.add(contractor_base)
        return contractor

    async def update_contractor(self, contractor: Contractor) -> Contractor:
        stmt = (
            update(ContractorBase)
            .where(ContractorBase.contractor_id == contractor.contractor_id)
            .values(about=contractor.about)
        )
        await self.executor.execute(stmt)
        return contractor
