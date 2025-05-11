from typing import Generic, Self
from sqlalchemy import Row, Select, select
from sqlalchemy.orm import aliased

from domain.dto.user.internal.user_filter_dto import (
    AdminFilterDTO,
    ContracteeFilterDTO,
    UserFilterDTO,
)
from infrastructure.database.models import (
    AdminBase,
    Base,
    ContracteeBase,
    ContractorBase,
    TelegramCredentialsBase,
    UserBase,
    WebCredentialsBase,
)
from infrastructure.repositories.base import O


def get_safe_attr(row: Row, model: type[Base]):
    """
    Возвращает атрибут строки из SQLAlchemy,
    соответсвующий имени `model`, или `None`, если не найден.
    """
    return getattr(row, model.__name__, None)


class UserQueryBuilder(Generic[O]):
    def __init__(self):
        self._entities = [UserBase]
        self._stmt = select(UserBase)

    def add_admin(self) -> Self:
        if AdminBase not in self._entities:
            self._entities.append(AdminBase)
            self._stmt = self._stmt.add_columns(AdminBase)
        return self.join_admin()

    def add_contractee(self) -> Self:
        if ContracteeBase not in self._entities:
            self._entities.append(ContracteeBase)
            self._stmt = self._stmt.add_columns(ContracteeBase)
        return self.join_contractee()

    def add_contractor(self) -> Self:
        if ContractorBase not in self._entities:
            self._entities.append(ContractorBase)
            self._stmt = self._stmt.add_columns(ContractorBase)
        return self.join_contractor()

    def add_credentials(self) -> Self:
        for model in [WebCredentialsBase, TelegramCredentialsBase]:
            if model not in self._entities:
                self._entities.append(model)
                self._stmt = self._stmt.add_columns(model)
        return self.join_credentials()

    def where_user_id(self, user_id: int) -> Self:
        self._stmt = self._stmt.where(UserBase.user_id == user_id)
        return self

    def join_admin(self) -> Self:
        self._stmt = self._stmt.outerjoin(
            AdminBase, UserBase.user_id == AdminBase.admin_id
        )
        return self

    def join_contractee(self) -> Self:
        self._stmt = self._stmt.outerjoin(
            ContracteeBase, UserBase.user_id == ContracteeBase.contractee_id
        )
        return self

    def join_contractor(self) -> Self:
        self._stmt = self._stmt.outerjoin(
            ContractorBase, UserBase.user_id == ContractorBase.contractor_id
        )
        return self

    def join_credentials(self) -> Self:
        self._stmt = self._stmt.outerjoin(
            WebCredentialsBase, UserBase.user_id == WebCredentialsBase.user_id
        ).outerjoin(
            TelegramCredentialsBase,
            UserBase.user_id == TelegramCredentialsBase.user_id,
        )
        return self

    def apply_contractee_filter(self, filter: ContracteeFilterDTO) -> Self:
        if filter.gender:
            self._stmt = self._stmt.where(
                ContracteeBase.gender == filter.gender
            )
        if filter.citizenship:
            self._stmt = self._stmt.where(
                ContracteeBase.citizenship == filter.citizenship
            )
        if filter.positions is not None:
            self._stmt = self._stmt.where(
                ContracteeBase.positions == filter.positions
            )
        return self.apply_user_filter(filter)

    def apply_admin_filter(self, filter: AdminFilterDTO) -> Self:
        return self.apply_user_filter(filter)

    def apply_contractor_filter(self, filter: AdminFilterDTO) -> Self:
        return self.apply_user_filter(filter)

    def apply_user_filter(self, filter: UserFilterDTO) -> Self:
        if filter.status:
            self._stmt = self._stmt.where(UserBase.status == filter.status)
        if filter.phone_number:
            self._stmt = self._stmt.where(
                UserBase.phone_number == filter.phone_number
            )
        if filter.role:
            self._stmt = self._stmt.where(UserBase.role == filter.role)
        if filter.last_id:
            self._stmt = self._stmt.where(UserBase.user_id > filter.last_id)
        if filter.size:
            self._stmt = self._stmt.limit(filter.size)
        return self

    def build(self) -> Select:
        return self._stmt
