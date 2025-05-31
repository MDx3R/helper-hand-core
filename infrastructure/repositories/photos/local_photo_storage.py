import os
from typing import BinaryIO

from domain.exceptions.base import RepositoryException
from domain.exceptions.service.common import NotFoundException
from domain.repositories.photo_storage import PhotoStorage


class LocalPhotoStorage(PhotoStorage):
    def __init__(self, base_dir: str = "uploads"):  # TODO: config
        os.makedirs(base_dir, exist_ok=True)
        self.base_dir = base_dir

    async def save_photo(self, photo_id: str, content: BinaryIO) -> str:
        content.seek(0)
        try:
            file_path = self._concat_filename(photo_id)
            with open(file_path, "wb") as f:
                f.write(content.read())
            return photo_id
        except Exception as e:
            raise RepositoryException(f"Ошибка при сохранении фото: {e}")

    async def get_photo(self, photo_id: str) -> BinaryIO:
        file_path = self._concat_filename(photo_id)

        if not os.path.exists(file_path):
            raise NotFoundException(f"Фото '{photo_id}' не найдено")

        try:
            return open(file_path, "rb")
        except Exception as e:
            raise RepositoryException(f"Ошибка при открытии фото: {e}")

    async def remove_photo(self, photo_id: str) -> None:
        file_path = self._concat_filename(photo_id)

        if not os.path.exists(file_path):
            raise NotFoundException(f"Фото '{photo_id}' не найдено")

        try:
            os.remove(file_path)
        except Exception as e:
            raise RepositoryException(f"Ошибка при удалении фото: {e}")

    def _concat_filename(self, photo_id: str) -> str:
        return f"{os.path.join(self.base_dir, photo_id)}.jpeg"
