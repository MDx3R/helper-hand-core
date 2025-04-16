from datetime import date
from typing import List, Literal, Optional

from pydantic import Field

from domain.entities.enums import CitizenshipEnum, GenderEnum, PositionEnum

from .enums import RoleEnum
from .user import User


class Contractee(User):
    """
    Модель исполнителя, расширяющая модель `User`.
    """

    user_id: Optional[int] = Field(default=None, alias="contractee_id")
    """
    Уникальный идентификатор исполнителя.
    Наследуется от `user_id` родительского класса `User`, переопределен под другим именем атрибута `contractee_id`.
    Может быть `None` при создании нового исполнителя.
    """

    birthday: date
    height: int
    gender: GenderEnum
    citizenship: CitizenshipEnum
    positions: List[PositionEnum]

    role: Literal[RoleEnum.contractee] = RoleEnum.contractee
    """Роль исполнителя. Всегда имеет значение `RoleEnum.contractee`."""

    @property
    def contractee_id(self) -> int:
        """
        Возвращает идентификатор исполнителя `user_id`.
        """
        return self.user_id
