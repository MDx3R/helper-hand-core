from typing import List

from domain.dto.user.base import UserBaseDTO
from domain.entities.enums import RoleEnum, UserStatusEnum


class UserOutputDTO(UserBaseDTO):
    user_id: int
    photos: List[str]
    role: RoleEnum
    status: UserStatusEnum
