from typing import Optional

from domain.entities import TelegramUser
from domain.dto.input import UserInputDTO

class UserRegistrationDTO(UserInputDTO):
    user_id: None = None

class WebUserRegistrationDTO(UserRegistrationDTO):
    telegram_id: None = None
    chat_id: None = None

class TelegramUserRegistrationDTO(UserRegistrationDTO):
    telegram_id: int
    chat_id: int

    def to_telegram_user(self, user_id: int) -> TelegramUser:
        """
        Поле `user_id` должно быть установлено с целью поддержки целостности данных.
        """
        return TelegramUser(
            user_id=user_id, 
            telegram_id=self.telegram_id,
            chat_id=self.chat_id
        )

class UserResetDTO(UserInputDTO):
    user_id: int