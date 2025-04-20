from domain.dto.user.internal.base import UserIdDTO
from domain.entities.user.enums import UserStatusEnum


class SetUserStatusDTO(UserIdDTO):
    status: UserStatusEnum
