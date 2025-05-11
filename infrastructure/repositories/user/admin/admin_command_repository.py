from sqlalchemy import update
from domain.repositories.user.admin.admin_command_repository import (
    AdminCommandRepository,
)
from infrastructure.repositories.base import QueryExecutor

from domain.entities.user.admin.admin import Admin
from infrastructure.database.models import AdminBase


class AdminCommandRepositoryImpl(AdminCommandRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def create_admin(self, admin: Admin) -> Admin:
        admin_base = AdminBase(
            admin_id=admin.admin_id,
            about=admin.about,
            contractor_id=admin.contractor_id,
        )
        self.executor.add(admin_base)
        return admin

    async def update_admin(self, admin: Admin) -> Admin:
        stmt = (
            update(AdminBase)
            .where(AdminBase.admin_id == admin.admin_id)
            .values(
                about=admin.about,
                contractor_id=admin.contractor_id,
            )
        )
        await self.executor.execute(stmt)
        return admin
