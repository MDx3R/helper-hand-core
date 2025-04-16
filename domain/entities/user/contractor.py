from typing import Literal, Optional

from pydantic import Field

from .enums import RoleEnum
from .user import User


class Contractor(User):
    """
    Модель заказчика, расширяющая модель `User`.
    """

    user_id: Optional[int] = Field(default=None, alias="contractor_id")
    """
    Уникальный идентификатор заказчика.
    Наследуется от `user_id` родительского класса `User`, переопределен под другим именем атрибута `contractor_id`.
    Может быть `None` только при создании нового заказчика.
    """

    about: str

    role: Literal[RoleEnum.contractor] = RoleEnum.contractor
    """Роль заказчика. Всегда имеет значение `RoleEnum.contractor`."""

    @property
    def contractor_id(self) -> int:
        """
        Возвращает идентификатор заказчика `user_id`.
        """
        return self.user_id
