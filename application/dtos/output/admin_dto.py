from typing import Optional
from .user_dto import UserOutputDTO

from domain.entities import Admin
from domain.entities.enums import RoleEnum

class AdminOutputDTO(UserOutputDTO):
    """
    DTO выходных данных администратора.

    Этот класс используется для представления данных администратора на уровень представления.
    """

    about: str
    role: RoleEnum = RoleEnum.contractor
    contractor_id: Optional[int] = None
    
    @property
    def contractor_id(self) -> int:
        return self.user_id
    
    @classmethod
    def from_admin(cls, admin: Admin) -> 'AdminOutputDTO':
        """
        Преобразует `Admin` в `AdminOutputDTO`.
        """
        return cls(
            user_id=admin.user_id,
            surname=admin.surname,
            name=admin.name,
            patronymic=admin.patronymic,
            phone_number=admin.phone_number,
            role=admin.role,
            status=admin.status,
            photos=admin.photos,
            telegram_id=admin.telegram_id,
            chat_id=admin.chat_id,
            about=admin.about,
            contractor_id=admin.contractor_id
        )