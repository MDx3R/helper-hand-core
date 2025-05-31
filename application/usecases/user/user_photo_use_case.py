from typing import BinaryIO, List
from uuid import uuid4
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.upload_photo_dto import RemovePhotoDTO
from domain.dto.user.response.user_output_dto import UserOutputDTO
from domain.exceptions.base import ServiceException
from domain.exceptions.service.auth import UnauthorizedAccessException
from domain.exceptions.service.common import NotFoundException
from domain.mappers.user_mappers import UserMapper
from domain.repositories.photo_storage import PhotoStorage
from domain.repositories.user.user_command_repository import (
    UserCommandRepository,
)
from domain.repositories.user.user_query_repository import UserQueryRepository
from domain.services.domain.services import UserDomainService


class GetPhotoUseCase:
    def __init__(
        self,
        photo_storage: PhotoStorage,
        user_query_repository: UserQueryRepository,
    ) -> None:
        self.photo_storage = photo_storage
        self.user_query_repository = user_query_repository

    async def execute(self, photo_id: str) -> BinaryIO:
        return await self.photo_storage.get_photo(photo_id)


class UploadPhotoUseCase:
    def __init__(
        self,
        photo_storage: PhotoStorage,
        user_query_repository: UserQueryRepository,
        user_command_repository: UserCommandRepository,
    ) -> None:
        self.photo_storage = photo_storage
        self.user_query_repository = user_query_repository
        self.user_command_repository = user_command_repository

    async def execute(
        self, content: BinaryIO, context: UserContextDTO
    ) -> UserOutputDTO:
        user = await self.user_query_repository.get_user(context.user_id)
        if not user:
            raise ServiceException(
                "Непредвиденная ошибка: пользователь авторизован, но не найден"
            )
        if not UserDomainService.is_allowed_to_upload_photo(user):
            raise UnauthorizedAccessException(
                "Загрузка фотографий не разрешена."
            )

        photo_id = str(uuid4())
        await self.photo_storage.save_photo(photo_id, content)

        user.photos.append(photo_id)
        user = await self.user_command_repository.update_user(user)
        return UserMapper.to_output(user)


class RemovePhotoUseCase:
    def __init__(
        self,
        photo_storage: PhotoStorage,
        user_query_repository: UserQueryRepository,
        user_command_repository: UserCommandRepository,
    ) -> None:
        self.photo_storage = photo_storage
        self.user_query_repository = user_query_repository
        self.user_command_repository = user_command_repository

    async def execute(self, request: RemovePhotoDTO) -> UserOutputDTO:
        user = await self.user_query_repository.get_user(
            request.context.user_id
        )
        if not user:
            raise ServiceException(
                "Непредвиденная ошибка: пользователь авторизован, но не найден"
            )
        if request.photo_id not in user.photos:
            raise NotFoundException(request.photo_id)

        await self.photo_storage.remove_photo(request.photo_id)

        user.photos.remove(request.photo_id)
        user = await self.user_command_repository.update_user(user)
        return UserMapper.to_output(user)


class GetUserAvatarUseCase:
    def __init__(
        self,
        photo_storage: PhotoStorage,
        user_query_repository: UserQueryRepository,
    ) -> None:
        self.photo_storage = photo_storage
        self.user_query_repository = user_query_repository

    async def execute(self, user_id: int) -> BinaryIO:
        user = await self.user_query_repository.get_user(user_id)
        if not user:
            raise NotFoundException(user_id)

        avatar_id = UserDomainService.get_avatar_photo_id(user)
        if not avatar_id:
            raise NotFoundException("Аватар не найден")

        return await self.photo_storage.get_photo(avatar_id)


class GetUserPhotosUseCase:
    def __init__(
        self,
        photo_storage: PhotoStorage,
        user_query_repository: UserQueryRepository,
    ) -> None:
        self.photo_storage = photo_storage
        self.user_query_repository = user_query_repository

    async def execute(self, user_id: int) -> List[BinaryIO]:
        user = await self.user_query_repository.get_user(user_id)
        if not user:
            raise NotFoundException(user_id)

        return [
            await self.photo_storage.get_photo(photo_id)
            for photo_id in user.photos
        ]
