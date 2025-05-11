from dataclasses import dataclass
from typing import Optional, Tuple
from sqlalchemy import Select, select
from domain.entities.user.admin.admin import Admin
from domain.entities.user.admin.composite_admin import CompleteAdmin
from domain.entities.user.contractee.composite_contractee import (
    CompleteContractee,
)
from domain.entities.user.contractee.contractee import Contractee
from domain.entities.user.contractor.composite_contractor import (
    CompleteContractor,
)
from domain.entities.user.contractor.contractor import Contractor
from domain.entities.user.enums import RoleEnum
from domain.repositories.user.user_role_query_repository import (
    UserRoleQueryRepository,
)
from infrastructure.database.mappers import AggregatedUserMapper
from infrastructure.database.models import (
    AdminBase,
    ContracteeBase,
    ContractorBase,
    TelegramCredentialsBase,
    UserBase,
    WebCredentialsBase,
)
from infrastructure.repositories.base import O, QueryExecutor


@dataclass
class UnmapperUser:
    user: UserBase
    admin: Optional[AdminBase]
    contractee: Optional[ContracteeBase]
    contractor: Optional[ContractorBase]
    web: Optional[WebCredentialsBase]
    telegram: Optional[TelegramCredentialsBase]

    @property
    def role(self):
        match self.user.role:
            case RoleEnum.admin:
                result = self.admin
            case RoleEnum.contractee:
                result = self.contractee
            case RoleEnum.contractor:
                result = self.contractor
            case _:
                result = None

        if not result:
            raise Exception(
                f"Роль пользователя {self.user.user_id} не отсутсвует таблице"
            )

        return result


class UserRoleQueryRepositoryImpl(UserRoleQueryRepository):
    def __init__(self, executor: QueryExecutor):
        self.executor = executor

    async def get_user(
        self, user_id: int
    ) -> Admin | Contractee | Contractor | None:
        stmt = select(UserBase, AdminBase, ContracteeBase, ContractorBase)
        stmt = self._join_roles(stmt)

        row = (await self.executor.execute(stmt)).first()
        if not row:
            return None

        unmapped_user = await self._execute_first(stmt)

        return AggregatedUserMapper.to_model(
            unmapped_user.user, unmapped_user.role
        )

    async def get_complete_user(
        self, user_id: int
    ) -> CompleteAdmin | CompleteContractee | CompleteContractor | None:
        stmt = select(
            UserBase,
            AdminBase,
            ContracteeBase,
            ContractorBase,
            WebCredentialsBase,
            TelegramCredentialsBase,
        )
        stmt = self._join_roles(stmt)
        stmt = self._join_credentials(stmt)

        unmapped_user = await self._execute_first(stmt)

        return  # TODO: Mapper

    async def get_first_pending_user(
        self,
    ) -> CompleteContractee | CompleteContractor | None:
        stmt = select(
            UserBase,
            ContracteeBase,
            ContractorBase,
            WebCredentialsBase,
            TelegramCredentialsBase,
        )
        stmt = self._join_contractee(stmt)
        stmt = self._join_contractor(stmt)

        unmapped_user = await self._execute_first(stmt)

        return  # TODO: Mapper

    async def _execute_first(self, statement: Select) -> UnmapperUser | None:
        row = (await self.executor.execute(statement)).first()
        if not row:
            return None

        return UnmapperUser(*row.tuple())

    def _join_roles(self, statement: Select[O]) -> Select[O]:
        stmt = self._join_admin(statement)
        stmt = self._join_contractee(stmt)
        stmt = self._join_contractor(stmt)
        return stmt

    def _join_admin(self, statement: Select[O]) -> Select[O]:
        return statement.outerjoin(
            AdminBase, UserBase.user_id == AdminBase.admin_id
        )

    def _join_contractee(self, statement: Select[O]) -> Select[O]:
        return statement.outerjoin(
            ContracteeBase,
            UserBase.user_id == ContracteeBase.contractee_id,
        )

    def _join_contractor(self, statement: Select[O]) -> Select[O]:
        return statement.outerjoin(
            ContractorBase,
            UserBase.user_id == ContractorBase.contractor_id,
        )

    def _join_credentials(self, statement: Select[O]) -> Select[O]:
        return statement.outerjoin(
            WebCredentialsBase,
            UserBase.user_id == WebCredentialsBase.user_id,
        ).outerjoin(
            TelegramCredentialsBase,
            UserBase.user_id == TelegramCredentialsBase.user_id,
        )
