from domain.entities.base import ApplicationModel
from domain.entities.user.credentials import UserCredentials
from domain.entities.user.enums import RoleEnum, UserStatusEnum


class UserContext(ApplicationModel):
    user_id: int
    role: RoleEnum
    status: UserStatusEnum
    credentials: UserCredentials
