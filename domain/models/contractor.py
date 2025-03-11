from typing import Optional
from pydantic import Field

from .enums import RoleEnum
from .user import User

class Contractor(User):
    """
    Модель заказчика, расширяющая модель `User`.

    Представляет данные заказчика, включая дополнительную информацию.
    """

    user_id: Optional[int] = Field(default=None, alias="contractor_id")
    """
    Уникальный идентификатор заказчика.
    Наследуется от `user_id` родительского класса `User`, переопределен под другим именем атрибута `contractor_id`.
    Может быть `None` при создании нового заказчика.
    """

    about: str
    """Информация о заказчике."""
    
    role: RoleEnum = RoleEnum.contractor
    """Роль заказчика. Всегда имеет значение `RoleEnum.contractor`."""

    @property
    def contractor_id(self) -> int:
        """
        Возвращает идентификатор заказчика.

        Это свойство обеспечивает доступ к `user_id` через имя `contractor_id`.
        """
        return self.user_id