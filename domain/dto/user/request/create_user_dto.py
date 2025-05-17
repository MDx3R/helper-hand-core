from domain.dto.user.request.user_input_dto import WithCredentialsInputDTO
from domain.entities.user.enums import UserStatusEnum


class BaseCreateUserDTO(WithCredentialsInputDTO):
    status: UserStatusEnum = UserStatusEnum.registered


class CreateCredentialsDTO(WithCredentialsInputDTO):
    user_id: int
