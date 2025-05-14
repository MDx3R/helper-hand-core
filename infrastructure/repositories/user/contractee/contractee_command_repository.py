from sqlalchemy import update
from domain.repositories.user.contractee.contractee_command_repository import (
    ContracteeCommandRepository,
)
from infrastructure.database.mappers import ContracteeMapper
from infrastructure.repositories.base import QueryExecutor

from domain.entities.user.contractee.contractee import Contractee
from infrastructure.database.models import ContracteeBase, UserBase


class ContracteeCommandRepositoryImpl(ContracteeCommandRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def create_contractee(self, contractee: Contractee) -> Contractee:
        async with self.executor.transaction_manager.get_session() as session:
            user_base = ContracteeMapper.to_user_base(contractee)
            await self.executor.add(user_base)
            contractee_base = ContracteeMapper.to_role_base(contractee)
            contractee_base.contractee_id = user_base.user_id
            await self.executor.add(contractee_base)
        return ContracteeMapper.to_model(user_base, contractee_base)

    async def update_contractee(self, contractee: Contractee) -> Contractee:
        stmt = (
            update(UserBase)
            .where(UserBase.user_id == contractee.user_id)
            .values(
                ContracteeMapper.to_user_base(contractee).get_fields(),
            )
        )
        await self.executor.execute(stmt)
        stmt = (
            update(ContracteeBase)
            .where(ContracteeBase.contractee_id == contractee.contractee_id)
            .values(
                ContracteeMapper.to_role_base(contractee).get_fields(),
            )
        )
        await self.executor.execute(stmt)
        return contractee
