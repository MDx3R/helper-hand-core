from domain.dto.base import InternalDTO


class UserIdDTO(InternalDTO):
    user_id: int


class PhoneNumberDTO(InternalDTO):
    number: str
