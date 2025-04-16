from domain.dto.user.base import TelegramCredentialsDTO
from domain.dto.user.request.user_input_dto import UserInputDTO


class UserRegistrationDTO(UserInputDTO):
    pass


class WebUserRegistrationDTO(UserRegistrationDTO):
    pass


class TelegramUserRegistrationDTO(UserRegistrationDTO, TelegramCredentialsDTO):
    pass


class UserResetDTO(UserInputDTO):
    user_id: int
