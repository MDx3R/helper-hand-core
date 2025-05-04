from abc import ABC, abstractmethod
from typing import List

from domain.dto.reply.internal.reply_query_dto import (
    GetContracteeRepliesDTO,
    GetReplyDTO,
)
from domain.dto.reply.request.create_reply_dto import CreateReplyDTO
from domain.dto.reply.response.reply_output_dto import ReplyOutputDTO
from domain.entities.reply.composite_reply import CompleteReply


class ContracteeReplyManagmentService(ABC):
    @abstractmethod
    async def submit_reply(self, request: CreateReplyDTO) -> ReplyOutputDTO:
        """
        Создает новый отклик на заказ.

        Основные аспекты:
        - Отклик исполнителя на заказ требует подтверждения заказчиком.
        - Отклик может быть отправлен только на открытый заказ.
        - Отклик может быть отправлен только на позицию, для которой есть свободные места.
        - Отклик не может быть отправлен повторно.
        - Отклик не может быть отправлен на дату, которая уже прошла или которая занята другим подтвержденным откликом.
        - На одну дату может быть отправлено много откликов. Подтверждается только один.
        - После успешного создания отклика отправляется уведомление заказчику.

        Args:
            reply_input (ReplyInputDTO): DTO с данными для создания отклика.

        Returns:
            DetailedReplyDTO: DTO с данными созданного отклика.

        Raises:
            InvalidReplyException: Возникает, если отклик не может быть отправлен.
            IntegrityException: Возникает при нарушении целостности данных.
        """
        pass


class ContracteeReplyService(ABC):
    """
    Интерфейс для сервисов откликов исполнителя.

    Этот класс определяет интерфейс для сервисов, отвечающих за возможности исполнителя по управлению откликами.
    """

    @abstractmethod
    async def get_reply(self, query: GetReplyDTO) -> CompleteReply | None:
        """
        Получает отклик.

        Args:
            contractee_id (int): ID исполнителя.
            detail_id (int): ID позиции.
            contractee (Contractee): Объект исполнителя.

        Returns:
            DetailedReplyDTO: DTO с данными отклика. Может быть `None`, если был запрошен чужой отклик или отклика не существует.
        """
        pass

    @abstractmethod
    async def get_future_replies(
        self, query: GetContracteeRepliesDTO
    ) -> List[ReplyOutputDTO]:
        pass
