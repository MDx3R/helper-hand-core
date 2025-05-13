from sqlalchemy import update
from domain.repositories.user.admin.admin_command_repository import (
    AdminCommandRepository,
)
from infrastructure.database.mappers import AdminMapper, UserMapper
from infrastructure.repositories.base import QueryExecutor

from domain.entities.user.admin.admin import Admin
from infrastructure.database.models import AdminBase, UserBase


class AdminCommandRepositoryImpl(AdminCommandRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def create_admin(self, admin: Admin) -> Admin:
        async with self.executor.transaction_manager.get_session() as session:
            user_base = AdminMapper.to_user_base(admin)
            self.executor.add(user_base)
            admin_base = AdminMapper.to_role_base(admin)
            admin_base.admin_id = user_base.user_id
            self.executor.add(admin_base)
        return AdminMapper.to_model(user_base, admin_base)

    async def update_admin(self, admin: Admin) -> Admin:
        stmt = (
            update(UserBase)
            .where(UserBase.user_id == admin.user_id)
            .values(
                AdminMapper.to_user_base(admin).get_fields(),
            )
        )
        await self.executor.execute(stmt)
        stmt = (
            update(AdminBase)
            .where(AdminBase.admin_id == admin.user_id)
            .values(
                AdminMapper.to_role_base(admin).get_fields(),
            )
        )
        await self.executor.execute(stmt)
        return admin
