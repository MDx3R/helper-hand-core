from typing import Any, List, Optional

from domain.entities.base import ApplicationModel

from .enums import RoleEnum, UserStatusEnum


class User(ApplicationModel):
    """
    Модель пользователя.
    """

    user_id: Optional[int] = None
    """Уникальный идентификатор пользователя. Может быть `None` только при создании нового пользователя."""

    surname: str
    name: str
    patronymic: Optional[str] = None
    phone_number: str
    role: RoleEnum
    status: UserStatusEnum = UserStatusEnum.created

    photos: List[str]
    """Доступ к фотографиям пользователя. Фотография может быть не установлена."""

    def get_fields(self) -> dict[str, Any]:
        """
        К полям класса добавится `user_id`,
        так как для производных моделей пользователя используется alias для `user_id`.
        """
        data = super().get_fields()
        data["user_id"] = self.user_id
        return data
