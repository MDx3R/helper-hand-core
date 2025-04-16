from typing import Literal, Optional

from pydantic import Field

from .enums import RoleEnum
from .user import User


class Admin(User):
    """
    Модель администратора, расширяющая модель `User`.
    """

    user_id: Optional[int] = Field(default=None, alias="admin_id")
    """
    Уникальный идентификатор администратора.
    Наследуется от `user_id` родительского класса `User`, переопределен под другим именем атрибута `admin_id`.
    Может быть `None` при создании нового администратора.
    """

    about: str

    role: Literal[RoleEnum.admin] = RoleEnum.admin
    """Роль администратора. Всегда имеет значение `RoleEnum.admin`."""

    contractor_id: Optional[int] = None
    """
    Прокси профиль администратора для создания заказов. 
    Указывает, является ли администратор заказчиком (имеет профиль заказчика) и может ли он создавать заказы.
    """

    @property
    def admin_id(self) -> int:
        """
        Возвращает идентификатор администратора `user_id`.
        """
        return self.user_id
