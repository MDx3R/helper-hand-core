from domain.dto.base import InternalDTO
from domain.dto.user.base import TelegramCredentialsDTO


class UserIdDTO(InternalDTO):
    user_id: int


class PhoneNumberDTO(InternalDTO):
    number: str


class UserWithCredentialsDTO(InternalDTO):
    telegram: TelegramCredentialsDTO
    # TODO: Добавить WebCredentialsDTO
