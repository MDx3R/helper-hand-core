from typing import BinaryIO, List
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.upload_photo_dto import RemovePhotoDTO
from domain.dto.user.response.user_output_dto import UserOutputDTO
from application.usecases.user.user_photo_use_case import (
    GetPhotoUseCase,
    UploadPhotoUseCase,
    RemovePhotoUseCase,
)
from domain.services.user_photo_service import PhotoService


class PhotoServiceImpl(PhotoService):
    def __init__(
        self,
        get_photo_use_case: GetPhotoUseCase,
        upload_photo_use_case: UploadPhotoUseCase,
        remove_photo_use_case: RemovePhotoUseCase,
    ) -> None:
        self.get_photo_use_case = get_photo_use_case
        self.upload_user_photos_use_case = upload_photo_use_case
        self.remove_user_photo_use_case = remove_photo_use_case

    async def get_photo(self, photo_id: str) -> BinaryIO:
        return await self.get_photo_use_case.execute(photo_id)

    async def upload_photo(
        self, content: BinaryIO, context: UserContextDTO
    ) -> UserOutputDTO:
        return await self.upload_user_photos_use_case.execute(content, context)

    async def remove_photo(self, request: RemovePhotoDTO) -> UserOutputDTO:
        return await self.remove_user_photo_use_case.execute(request)
