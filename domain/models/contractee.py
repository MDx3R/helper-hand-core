from typing import Optional, List
from datetime import date
from pydantic import Field

from .enums import RoleEnum, GenderEnum, CitizenshipEnum, PositionEnum
from .user import User

class Contractee(User):
    """
    Модель исполнителя, расширяющая модель `User`.

    Представляет данные исполнителя, включая дату рождения, рост, пол,
    гражданство, доступные позиции и фото.
    """

    user_id: Optional[int] = Field(default=None, alias="contractee_id")
    """
    Уникальный идентификатор исполнителя.
    Наследуется от `user_id` родительского класса `User`, переопределен под другим именем атрибута `contractee_id`.
    Может быть `None` при создании нового исполнителя.
    """

    birthday: date
    """Дата рождения исполнителя."""

    height: int
    """Рост исполнителя в сантиметрах."""

    gender: GenderEnum
    """Пол исполнителя."""

    citizenship: CitizenshipEnum
    """Гражданство исполнителя."""

    positions: List[PositionEnum]
    """Список возможных позиций, которые может занимать исполнитель."""

    role: RoleEnum = RoleEnum.contractee
    """Роль исполнителя. Всегда имеет значение `RoleEnum.contractee`."""

    @property
    def contractee_id(self) -> int:
        """
        Возвращает идентификатор исполнителя.

        Это свойство обеспечивает доступ к `user_id` через имя `contractee_id`.
        """
        return self.user_id