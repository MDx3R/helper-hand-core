from domain.dto.base import ApplicationDTO, InternalDTO
from domain.dto.user.base import TelegramCredentialsDTO
from domain.dto.user.response.user_output_dto import UserCredentialsOutputDTO


class UserIdDTO(InternalDTO):
    user_id: int


class PhoneNumberDTO(InternalDTO):
    number: str


class UserWithCredentialsDTO(ApplicationDTO):
    pass
