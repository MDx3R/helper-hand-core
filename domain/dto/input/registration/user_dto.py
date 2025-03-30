from typing import Optional

from domain.dto.input import UserInputDTO

class UserRegistrationDTO(UserInputDTO):
    user_id: None = None

class WebUserRegistrationDTO(UserRegistrationDTO):
    telegram_id: None = None
    chat_id: None = None

class TelegramUserRegistrationDTO(UserRegistrationDTO):
    telegram_id: int
    chat_id: int

class UserResetDTO(UserInputDTO):
    user_id: int