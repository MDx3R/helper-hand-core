from typing import Optional, List

from domain.entities import User 
from domain.entities.enums import RoleEnum, UserStatusEnum
from domain.entities.base import ApplicationModel

class UserInputDTO(ApplicationModel):
    user_id: int
    surname: str
    name: str
    patronymic: Optional[str] = None
    phone_number: str
    photos: List[str]

    def to_user(self) -> User:
        """
        Полю `role` назначается `RoleEnum.unset`. 
        Поле `status` устанавливается значением по умолчанию.
        """
        return User.model_validate(self.model_dump() | {"role": RoleEnum.unset})
    
class UserUpdateDTO(UserInputDTO):
    pass