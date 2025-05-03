from typing import Optional
from domain.entities.base import ApplicationModel
from domain.entities.user.user import User


class WebCredentials(ApplicationModel):
    """
    Модель пользователя из Web.

    Связывает пользователя: его id и учетные данные.
    """

    user_id: int
    email: str
    password: str


class TelegramCredentials(ApplicationModel):
    """
    Модель пользователя из Telegram.

    Связывает пользователя: его id и чат в Telegram.
    `telegram_id` и `chat_id` являются уникальными и предоставляются Telegram API.
    """

    user_id: int
    telegram_id: int
    chat_id: int


class UserCredentials(ApplicationModel):
    telegram: Optional[TelegramCredentials] = None
    web: Optional[WebCredentials] = None


class UserWithCredentials(ApplicationModel):
    user: User
    credentials: UserCredentials
