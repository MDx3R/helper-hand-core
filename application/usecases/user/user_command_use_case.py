from domain.dto.input.registration import UserRegistrationDTO

from domain.entities import User, Contractee, Contractor, Admin
from domain.entities.enums import UserStatusEnum
from domain.dto.common import UserDTO, ContracteeDTO, ContractorDTO
from domain.dto.input.registration import (
    UserRegistrationDTO, 
    ContracteeRegistrationDTO, 
    ContractorRegistrationDTO
)
from domain.repositories import UserRepository
from domain.services.domain import UserDomainService
from domain.exceptions.service import (
    UserStatusChangeNotAllowedException, 
    NotFoundException,
    InvalidInputException
)

from application.transactions import transactional

from abc import ABC, abstractmethod

from domain.dto.mappers import map_user_to_dto

class SaveUserUseCase(ABC):
    def __init__(
        self, user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    @transactional
    async def save_user(self, user_input: UserRegistrationDTO) -> ContracteeDTO | ContractorDTO:
        user = self._cast_role_input_to_role(user_input)
        user = await self._save_user(user)
        return map_user_to_dto(user)
    
    def _cast_role_input_to_role(self, user_input: UserRegistrationDTO) -> Contractee | Contractor:
        if isinstance(user_input, ContracteeRegistrationDTO):
            return user_input.to_contractee()
        elif isinstance(user_input, ContractorRegistrationDTO):
            return user_input.to_contractor()
        raise InvalidInputException(
            f"Роль пользователя {user_input.role} не совпадает с типом передаваемого объекта {type(user_input)}"
        )
    
    async def _save_user(self, user: Contractee | Contractor | Admin):
        return await self.user_repository.save(user)


class ChangeUserStatusUseCase(ABC):
    @abstractmethod
    async def change_user_status(self, user_id: int, status: UserStatusEnum) -> UserDTO:
        pass


class ApproveUserUseCase(ABC):
    @abstractmethod
    async def approve_user(self, user_id: int) -> UserDTO:
        pass


class DisapproveUserUseCase(ABC):
    @abstractmethod
    async def disapprove_user(self, user_id: int) -> UserDTO:
        pass


class DropUserUseCase(ABC):
    @abstractmethod
    async def drop_user(self, user_id: int) -> UserDTO:
        pass


class BanUserUseCase(ABC):
    @abstractmethod
    async def ban_user(self, user_id: int) -> UserDTO:
        pass


class UserCommandUseCase(
    ApproveUserUseCase, 
    DisapproveUserUseCase, 
    DropUserUseCase, 
    BanUserUseCase, 
    #ChangeUserStatusUseCase
):
    """
    Реализация Use Cases типа UserCommand.
    Не для прямого использования. 
    """
    def __init__(
        self, user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def approve_user(self, user_id: int) -> UserDTO:
        return await self.change_user_status(user_id, UserStatusEnum.registered)

    async def disapprove_user(self, user_id: int) -> UserDTO:
        return await self.change_user_status(user_id, UserStatusEnum.dropped)

    async def drop_user(self, user_id: int) -> UserDTO:
        return await self.change_user_status(user_id, UserStatusEnum.dropped)

    async def ban_user(self, user_id: int) -> UserDTO:
        return await self.change_user_status(user_id, UserStatusEnum.banned)

    @transactional
    async def change_user_status(self, user_id: int, status: UserStatusEnum) -> UserDTO:
        user = await self._get_user_with_role_and_raise_if_not_exists(user_id)

        user = await self._change_user_status(user, status)

        return UserDTO.from_user(user)
    
    async def _get_user_with_role_and_raise_if_not_exists(self, user_id: int) -> User:
        user = await self.user_repository.get_user_with_role(user_id)
        if not user:
            return NotFoundException(user_id)
        return user
        
    async def _change_user_status(self, user: User, status: UserStatusEnum) -> User:
        self._check_user_status_can_be_changed(user, status)
        
        return await self.user_repository.change_user_status(user.user_id, status)
    
    def _check_user_status_can_be_changed(self, user: User, status: UserStatusEnum):
        if not UserDomainService.can_status_be_changed(user, status):
            raise UserStatusChangeNotAllowedException(
                user.user_id, status, 
                "Статус пользователя не может быть изменен."
            )