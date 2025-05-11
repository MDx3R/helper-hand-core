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
from domain.entities.user.enums import RoleEnum, UserStatusEnum
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
from infrastructure.repositories.user.base import (
    UserQueryBuilder,
    get_safe_attr,
)


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
        query_builder = UserQueryBuilder()
        stmt = (
            query_builder.add_admin()
            .add_contractee()
            .add_contractor()
            .where_user_id(user_id)
            .build()
        )

        unmapped_user = await self._execute_first(stmt)
        if not unmapped_user:
            return None

        return AggregatedUserMapper.to_model(
            unmapped_user.user, unmapped_user.role
        )

    async def get_complete_user(
        self, user_id: int
    ) -> CompleteAdmin | CompleteContractee | CompleteContractor | None:
        query_builder = UserQueryBuilder()
        stmt = (
            query_builder.add_admin()
            .add_contractee()
            .add_contractor()
            .add_credentials()
            .where_user_id(user_id)
            .build()
        )

        unmapped_user = await self._execute_first(stmt)
        return  # TODO: Mapper

    async def get_first_pending_user(
        self,
    ) -> CompleteContractee | CompleteContractor | None:
        query_builder = UserQueryBuilder()
        stmt = (
            query_builder.add_contractee()
            .add_contractor()
            .add_credentials()
            .build()
            .where(UserBase.status == UserStatusEnum.pending)
            .limit(1)
        )

        unmapped_user = await self._execute_first(stmt)
        return  # TODO: Mapper

    async def _execute_first(self, statement: Select) -> UnmapperUser | None:
        row = (await self.executor.execute(statement)).first()
        if not row:
            return None

        return UnmapperUser(
            user=get_safe_attr(row, UserBase),
            admin=get_safe_attr(row, AdminBase),
            contractee=get_safe_attr(row, ContracteeBase),
            contractor=get_safe_attr(row, ContractorBase),
            web=get_safe_attr(row, WebCredentialsBase),
            telegram=get_safe_attr(row, TelegramCredentialsBase),
        )
