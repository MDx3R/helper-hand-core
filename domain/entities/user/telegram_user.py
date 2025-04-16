from domain.entities.base import ApplicationModel


class TelegramUser(ApplicationModel):
    """
    Модель пользователя из Telegram.

    Связывает пользователя и его id и чат в Telegram.
    `telegram_id` и `chat_id` являются уникальными и предоставляются Telegram API.
    """

    user_id: int
    telegram_id: int
    chat_id: int
