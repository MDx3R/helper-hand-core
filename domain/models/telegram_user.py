from .base import ApplicationModel

class TelegramUser(ApplicationModel):
    """
    Модель пользователя из Telegram.

    Связывает пользователя и его id и чат в Telegram. 
    `telegram_id` и `chat_id` являются уникальными и предоставляются Telegram API.
    """

    user_id: int
    """Уникальный идентификатор пользователя из `User`."""

    telegram_id: int 
    """Уникальный идентификатор пользователя в Telegram."""

    chat_id: int
    """Уникальный идентификатор чата с пользователем в Telegram."""