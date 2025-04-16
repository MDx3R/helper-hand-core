from typing import List

from domain.dto.user.base import UserBaseDTO


class UserInputDTO(UserBaseDTO):
    phone_number: str
    photos: List[str]
