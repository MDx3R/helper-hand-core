from abc import ABC, abstractmethod
from typing import BinaryIO


class PhotoStorage(ABC):
    @abstractmethod
    async def save_photo(self, photo_id: str, content: BinaryIO) -> str:
        """Сохраняет фото, возвращает строку доступа"""
        pass

    @abstractmethod
    async def remove_photo(self, photo_id: str) -> None:
        pass

    @abstractmethod
    async def get_photo(self, photo_id: str) -> BinaryIO:
        pass
