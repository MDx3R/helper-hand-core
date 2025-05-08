from domain.dto.base import ApplicationDTO
from domain.dto.user.request.user_input_dto import UserInputDTO


class UserRegistrationDTO(UserInputDTO):
    pass


class UserResetDTO(UserInputDTO):
    user_id: int


class LoginUserDTO(ApplicationDTO):
    email: str
    password: str
