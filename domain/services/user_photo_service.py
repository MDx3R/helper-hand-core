from abc import ABC, abstractmethod
from typing import BinaryIO

from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.upload_photo_dto import RemovePhotoDTO
from domain.dto.user.response.user_output_dto import UserOutputDTO


class PhotoService(ABC):
    @abstractmethod
    async def get_photo(self, photo_id: str) -> BinaryIO: ...
    @abstractmethod
    async def upload_photo(
        self, content: BinaryIO, context: UserContextDTO
    ) -> UserOutputDTO: ...
    @abstractmethod
    async def remove_photo(self, request: RemovePhotoDTO) -> UserOutputDTO: ...
