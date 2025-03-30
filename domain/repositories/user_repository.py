from typing import List
from abc import ABC, abstractmethod

from domain.entities import User, Admin, Contractee, Contractor, TelegramUser
from domain.entities.enums import UserStatusEnum, RoleEnum, GenderEnum

class UserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Получает пользователя по его ID.
        
        Args:
            user_id (int): ID пользователя.
            
        Returns:
            User: Модель с данными пользователя или `None`, если пользователь не найден.
        """
        pass
    
    @abstractmethod
    async def get_user_by_telegram_id(self, telegram_id: int) -> User | None:
        """
        Получает пользователя по его ID в Telegram. 
        
        Args:
            telegram_id (int): ID пользователя в Telegram.
            
        Returns:
            User: Модель с данными пользователя или `None`, если пользователь не найден.
        """
        pass
    
    @abstractmethod
    async def get_user_with_role(self, user_id: int) -> User | None:
        """
        Получает роль пользователя по его ID.
        
        Args:
            user_id (int): ID пользователя.
            
        Returns:
            User: Модель роли, расширяющая User.
        """
        pass

    @abstractmethod
    async def get_admin_by_id(self, admin_id: int) -> Admin | None:
        """
        Получает администратора по его ID.
        
        Args:
            admin_id (int): ID администратора.
        
        Returns:
            Admin: Модель с данными администратора или `None`, если администратор не найден.
        """
        pass
    
    @abstractmethod
    async def get_contractee_by_id(self, contractee_id: int) -> Contractee | None:
        """
        Получает исполнителя по его ID.
        
        Args:
            contractee_id (int): ID исполнителя.
        
        Returns:
            Contractee: Модель с данными исполнителя или `None`, если исполнитель не найден.
        """
        pass
    
    @abstractmethod
    async def get_contractor_by_id(self, contractor_id: int) -> Contractor | None:
        """
        Получает заказчика по его ID.
        
        Args:
            contractor_id (int): ID заказчика.
        
        Returns:
            Contractor: Модель с данными заказчика или `None`, если подрядчик не найден.
        """
        pass
    
    @abstractmethod
    async def get_admins(self) -> List[Admin]:
        """
        Получает список администраторов.
        
        Returns:
            List[Admin]: Список объектов администраторов.
        """
        pass

    @abstractmethod
    async def get_first_pending_user_with_role(self) -> User | None:
        """
        Получает первого пользователя, ждущего подтверждение регистрации.
            
        Returns:
            User: Модель роли, расширяющей User.
        """
        pass

    @abstractmethod
    async def save_telegram_user(self, user: TelegramUser) -> TelegramUser:
        """
        Сохраняет данные профиля Telegram пользователя.
        
        Args:
            user (TelegramUser)
        
        Returns:
            TelegramUser.
            
        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных.
            DuplicateEntryException: Возникает, если уникальные значения повторяются: Если произошел конфликт уникальности поля.
        """
        pass

    @abstractmethod
    async def save(self, role: Contractee | Contractor | Admin) -> Contractee | Contractor | Admin:
        """
        Сохраняет данные исполнителя, заказчика или администратора.
        
        Args:
            role (Contractee | Contractor | Admin): Модель с данными пользователя.
        
        Returns:
            Contractee | Contractor | Admin: Сохраненная модель пользователя.
            
        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных.
            DuplicateEntryException: Возникает, если уникальные значения повторяются: Если произошел конфликт уникальности поля.
        """
        pass

    @abstractmethod
    async def save_contractee(self, contractee: Contractee) -> Contractee:
        """
        Сохраняет данные исполнителя.
        
        Args:
            contractee (Contractee): Модель с данными исполнителя.
        
        Returns:
            Contractee: Сохраненная модель исполнителя.
            
        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных.
            DuplicateEntryException: Возникает, если уникальные значения повторяются: Если произошел конфликт уникальности поля.
        """
        pass
    
    @abstractmethod
    async def save_contractor(self, contractor: Contractor) -> Contractor:
        """
        Сохраняет данные заказчика.
        
        Args:
            contractor (Contractor): Модель с данными заказчика.
        
        Returns:
            Contractor: Сохраненная модель заказчика.
            
        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных.
            DuplicateEntryException: Возникает, если уникальные значения повторяются: Если произошел конфликт уникальности поля.
        """
        pass

    @abstractmethod
    async def save_admin(self, admin: Admin) -> Admin:
        """
        Сохраняет данные администратора.
        
        Args:
            admin (Admin): Модель с данными администратора.
        
        Returns:
            Admin: Сохраненная модель администратора.
            
        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных.
            DuplicateEntryException: Возникает, если уникальные значения повторяются: Если произошел конфликт уникальности поля.
        """
        pass
    
    @abstractmethod
    async def change_user_status(self, user_id: int, status: UserStatusEnum) -> User:
        """
        Изменяет статус пользователя.
        
        Args:
            user_id (int): ID пользователя.
            status (UserStatusEnum): новый статус пользователя.
            
        Returns:
            User: Изменённый пользователь.

        Raises:
            IntegrityException: Возникает при нарушении целостности данных при сохранении данных.
        """
        pass

    @abstractmethod
    async def user_exists_by_phone_number(self, phone_number: str) -> bool:
        """
        Проверяет, существует ли пользователь с данным номером телефона.
        
        Args:
            phone_number (str): Номер телефона пользователя.
        
        Returns:
            bool: `True`, если пользователь существует, иначе `False`.
        """
        pass

    @abstractmethod
    async def filter_contractees_by(self, status: UserStatusEnum = None, gender: GenderEnum = None) -> List[Contractee]:
        """
        Возвращает отфильтрованный список исполнителей.
        
        Returns:
            List[Contractee]
        """
        # todo: реализовать батчевый подход к сбору данных
        pass