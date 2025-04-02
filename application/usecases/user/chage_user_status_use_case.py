from domain.entities import User
from domain.entities.enums import UserStatusEnum
from domain.dto.common import UserDTO

from domain.repositories import UserRepository
from domain.services.domain import UserDomainService
from domain.exceptions.service import (
    UserStatusChangeNotAllowedException, 
    NotFoundException,
)

from application.transactions import transactional

from domain.dto.internal import (
    ApproveUserDTO,
    DisapproveUserDTO,
    DropUserDTO,
    BanUserDTO
)

from abc import ABC, abstractmethod

class ApproveUserUseCase(ABC):
    @abstractmethod
    async def approve_user(self, request: ApproveUserDTO) -> UserDTO:
        pass


class DisapproveUserUseCase(ABC):
    @abstractmethod
    async def disapprove_user(self, request: DisapproveUserDTO) -> UserDTO:
        pass


class DropUserUseCase(ABC):
    @abstractmethod
    async def drop_user(self, request: DropUserDTO) -> UserDTO:
        pass


class BanUserUseCase(ABC):
    @abstractmethod
    async def ban_user(self, request: BanUserDTO) -> UserDTO:
        pass


class ChangeUserStatusUseCaseFacade(
    ApproveUserUseCase, 
    DisapproveUserUseCase, 
    DropUserUseCase, 
    BanUserUseCase, 
):
    def __init__(
        self, user_repository: UserRepository,
    ):
        self.user_repository = user_repository

    async def approve_user(self, request: ApproveUserDTO) -> UserDTO:
        return await self.change_user_status(request.user_id, UserStatusEnum.registered)

    async def disapprove_user(self, request: DisapproveUserDTO) -> UserDTO:
        return await self.change_user_status(request.user_id, UserStatusEnum.disapproved)

    async def drop_user(self, request: DropUserDTO) -> UserDTO:
        # TODO: Отменять все отклики
        return await self.change_user_status(request.user_id, UserStatusEnum.dropped)

    async def ban_user(self, request: BanUserDTO) -> UserDTO:
        # TODO: Отменять все отклики
        return await self.change_user_status(request.user_id, UserStatusEnum.banned)

    @transactional
    async def change_user_status(self, user_id: int, status: UserStatusEnum) -> UserDTO:
        user = await self._get_user_and_raise_if_not_exists(user_id)

        user = await self._change_user_status(user, status)

        return UserDTO.from_user(user)
    
    async def _get_user_and_raise_if_not_exists(self, user_id: int) -> User:
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise NotFoundException(user_id)
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