from application.transactions import transactional
from domain.dto.user.internal.user_command_dto import SetUserStatusDTO
from domain.dto.user.internal.user_managment_dto import (
    ApproveUserDTO,
    BanUserDTO,
    DisapproveUserDTO,
    DropUserDTO,
)
from domain.dto.user.response.user_output_dto import UserOutputDTO
from domain.entities.user.enums import UserStatusEnum
from domain.entities.user.user import User
from domain.exceptions.service import (
    NotFoundException,
    UserStatusChangeNotAllowedException,
)
from domain.mappers.user_mappers import UserMapper
from domain.repositories.user.user_command_repository import (
    UserCommandRepository,
)
from domain.repositories.user.user_query_repository import UserQueryRepository
from domain.services.domain import UserDomainService


class ChangeUserStatusUseCase:
    def __init__(
        self,
        query_repository: UserQueryRepository,
        command_repository: UserCommandRepository,
    ):
        self.query_repository = query_repository
        self.command_repository = command_repository

    @transactional
    async def execute(
        self, user_id: int, status: UserStatusEnum
    ) -> UserOutputDTO:
        user = await self._get_user_and_raise_if_not_exists(user_id)

        user = await self._change_user_status(user, status)

        return UserMapper.to_output(user)

    async def _get_user_and_raise_if_not_exists(self, user_id: int) -> User:
        user = await self.query_repository.get_user(user_id)
        if not user:
            raise NotFoundException(user_id)
        return user

    async def _change_user_status(
        self, user: User, status: UserStatusEnum
    ) -> User:
        self._check_user_status_can_be_changed(user, status)

        return await self.command_repository.set_user_status(
            SetUserStatusDTO(user_id=user.user_id, status=status)
        )

    def _check_user_status_can_be_changed(
        self, user: User, status: UserStatusEnum
    ):
        if not UserDomainService.can_status_be_changed(user, status):
            raise UserStatusChangeNotAllowedException(
                user.user_id,
                status,
                "Статус пользователя не может быть изменен.",
            )


class ApproveUserUseCase:
    def __init__(
        self,
        change_status_use_case: ChangeUserStatusUseCase,
    ):
        self.change_status_use_case = change_status_use_case

    async def execute(self, request: ApproveUserDTO) -> UserOutputDTO:
        return await self.change_status_use_case.execute(
            request.user_id, UserStatusEnum.registered
        )


class DisapproveUserUseCase:
    def __init__(
        self,
        change_status_use_case: ChangeUserStatusUseCase,
    ):
        self.change_status_use_case = change_status_use_case

    async def execute(self, request: DisapproveUserDTO) -> UserOutputDTO:
        return await self.change_status_use_case.execute(
            request.user_id, UserStatusEnum.disapproved
        )


class DropUserUseCase:
    def __init__(
        self,
        change_status_use_case: ChangeUserStatusUseCase,
    ):
        self.change_status_use_case = change_status_use_case

    @transactional
    async def execute(self, request: DropUserDTO) -> UserOutputDTO:
        return await self.change_status_use_case.execute(
            request.user_id, UserStatusEnum.dropped
        )


class BanUserUseCase:
    def __init__(
        self,
        change_status_use_case: ChangeUserStatusUseCase,
    ):
        self.change_status_use_case = change_status_use_case

    @transactional
    async def execute(self, request: BanUserDTO) -> UserOutputDTO:
        return await self.change_status_use_case.execute(
            request.user_id, UserStatusEnum.banned
        )
