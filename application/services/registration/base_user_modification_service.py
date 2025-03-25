from typing import TypeVar
from abc import ABC, abstractmethod

from domain.dto.input.registration import UserRegistrationDTO, ContracteeRegistrationDTO, ContractorRegistrationDTO
from domain.dto.common import UserDTO
from domain.dto.mappers import map_user_to_dto

from domain.repositories import UserRepository
from application.transactions import TransactionManager

from domain.entities import Contractee, Contractor
from domain.exceptions.service import InvalidInputException

U = TypeVar('U', Contractor, Contractee)

class BaseUserModificationService(ABC):
    """Базовый класс для сервисов регистрации и сброса пользователя."""

    def __init__(
        self,
        user_repository: UserRepository,
        transaction_manager: TransactionManager,
    ):
        self.user_repository = user_repository
        self.transaction_manager = transaction_manager

    @abstractmethod
    def _assign_status(self, user: U) -> U:
        """Этот метод определяет различия между регистрацией"""
        pass

    async def _post_modification_hook(self, user: U):
        """Переопределение этого метода добавил дополнительные действия после изменения пользователя"""
        pass

    async def _modify_user(self, user_input: UserRegistrationDTO, user_id: int | None = None) -> UserDTO:
        async with self.transaction_manager:
            user = await self._create_or_update_user(self._cast_to_role_input_dto(user_input, user_id))

        if self._post_modification_hook is not BaseUserModificationService._post_modification_hook:
            await self._post_modification_hook(user)

        return map_user_to_dto(user)

    async def _create_or_update_user(self, user: U) -> U:
        user = self._assign_status(user)
        return await self._save_user(user)

    async def _save_user(self, user: U) -> U:
        return await self.user_repository.save(user)

    def _cast_to_role_input_dto(self, user_input: UserRegistrationDTO, user_id: int | None = None) -> U:
        if isinstance(user_input, ContracteeRegistrationDTO):
            return user_input.to_contractee()
        elif isinstance(user_input, ContractorRegistrationDTO):
            return user_input.to_contractor()
        raise InvalidInputException(
            f"Роль пользователя {user_input.role} не совпадает с типом передаваемого объекта {type(user_input)}"
        )