from abc import ABC, abstractmethod
from typing import List

from domain.dto.reply.internal.reply_filter_dto import ReplyFilterDTO
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO


class ReplyQueryService(ABC):
    @abstractmethod
    async def filter_replies(
        self, query: ReplyFilterDTO
    ) -> List[ReplyOutputDTO]:
        """
        Получает список откликов исполнителя по его ID.

        Args:
            contractee (Contractee): Объект исполнителя.
            page (int): Номер страницы.
            size (int): Размер страницы. По умолчанию размер страницы равен 10.

        Returns:
            List[DetailedReplyDTO]: Список DTO с данными откликов.
        """
        pass
