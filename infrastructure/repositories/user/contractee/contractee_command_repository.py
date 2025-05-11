from sqlalchemy import update
from domain.repositories.user.contractee.contractee_command_repository import (
    ContracteeCommandRepository,
)
from infrastructure.repositories.base import QueryExecutor

from domain.entities.user.contractee.contractee import Contractee
from infrastructure.database.models import ContracteeBase


class ContracteeCommandRepositoryImpl(ContracteeCommandRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def create_contractee(self, contractee: Contractee) -> Contractee:
        contractee_base = ContracteeBase(
            contractee_id=contractee.contractee_id,
            birthday=contractee.birthday,
            height=contractee.height,
            gender=contractee.gender,
            citizenship=contractee.citizenship,
            positions=contractee.positions,
        )
        self.executor.add(contractee_base)
        return contractee

    async def update_contractee(self, contractee: Contractee) -> Contractee:
        stmt = (
            update(ContracteeBase)
            .where(ContracteeBase.contractee_id == contractee.contractee_id)
            .values(
                birthday=contractee.birthday,
                height=contractee.height,
                gender=contractee.gender,
                citizenship=contractee.citizenship,
                positions=contractee.positions,
            )
        )
        await self.executor.execute(stmt)
        return contractee
