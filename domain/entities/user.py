from typing import Optional, List, Any, Optional
from .base import ApplicationModel

from .enums import RoleEnum, UserStatusEnum

class User(ApplicationModel):
    """
    Модель пользователя.

    Представляет данные пользователя, включая персональную информацию, контактные данные,
    роль и статус. 
    `telegram_id` и `chat_id` являются уникальными и предоставляются Telegram API.
    """
    
    user_id: Optional[int] = None
    """Уникальный идентификатор пользователя. Может быть `None` при создании нового пользователя."""

    surname: str
    """Фамилия пользователя."""

    name: str
    """Имя пользователя."""

    patronymic: Optional[str] = None
    """Отчество пользователя (может отсутствовать)."""

    phone_number: str
    """Номер телефона пользователя."""
    
    role: RoleEnum 
    """Роль пользователя."""

    telegram_id: Optional[int] = None
    """Уникальный идентификатор пользователя в Telegram."""

    chat_id: Optional[int] = None
    """Уникальный идентификатор чата с пользователем в Telegram."""

    status: UserStatusEnum = UserStatusEnum.created
    """Статус пользователя. Определяется с использованием `UserStatusEnum`."""

    photos: List[str]
    """Доступ к фотографии пользователя. Фотография может быть не установлена."""

    def get_fields(self) -> dict[str, Any]:
        """
        К полям класса добавится `user_id`, 
        так как для производных моделей пользователя используется alias для `user_id`.
        """
        data = super().get_fields()
        data["user_id"] = self.user_id
        return data