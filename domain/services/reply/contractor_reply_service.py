from abc import ABC, abstractmethod

from domain.dto.reply.internal.reply_managment_dto import (
    ApproveReplyDTO,
    DisapproveReplyDTO,
)
from domain.dto.reply.internal.reply_query_dto import GetOrderReplyDTO
from domain.dto.reply.response.reply_output_dto import (
    CompleteReplyOutputDTO,
    ReplyOutputDTO,
)


class ContractorReplyManagmentService(ABC):
    @abstractmethod
    async def approve_reply(self, request: ApproveReplyDTO) -> ReplyOutputDTO:
        """
        Подтверждает отклик по его ID.

        Основные аспекты отмены заказа:
        - Отклик может быть подтвержден только для открытого заказа.
        - Отклик может быть подтвержден, только если его статус установлен как `ReplyStatusEnum.created`.
        - Отклик может быть подтвержден только позиции, для которой есть свободные места.
        - Все отклики исполнителя на туже дату отменяются.
        - Если после подтверждения отклика на позиции не осталось свободных мест, то все неподтверждённые отклики отменяются автоматически.
        Владельцы отмененных откликов получают соответствующие уведомления.
        - Если после подтверждения отклика на заказ не осталось свободных мест, заказчик и администратор получают соответствующее уведомление.
        Заказ автоматически закрывается. Все неподтверждённые отклики отменяются автоматически. Владельцы отмененных откликов получают соответствующие уведомления.
        - После успешного подтверждения отклика отправляется уведомление исполнителю.

        Args:
            reply_id (int): ID отклика.
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему откликам.

        Returns:
            DetailedReplyDTO: DTO с подробными данными отклика.

        Raises:
            Exception: Если произошла ошибка при подтверждении отклика.
        """
        pass

    @abstractmethod
    async def disapprove_reply(
        self, request: DisapproveReplyDTO
    ) -> ReplyOutputDTO:
        """
        Отклоняет отклик по его ID.

        Args:
            reply_id (int): ID отклика.
            contractor (Contractor): Объект заказчика. Используется для ограничения доступа заказчика к не принадлежащим ему откликам.

        Returns:
            DetailedReplyDTO: DTO с подробными данными отклика.

        Raises:
            Exception: Если произошла ошибка при отклонении отклика.
        """
        pass


class ContractorReplyService(ABC):
    """
    Абстрактный класс для сервисов откликов заказчика.

    Этот класс определяет интерфейс для сервисов, отвечающих за возможности заказчика по управлению откликами.
    """

    @abstractmethod
    async def get_pending_reply(
        self, query: GetOrderReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        """
        Получает первый неподтвержденный отклик, требующий подтверждения заказчика.

        Args:
            contractor (Contractor): Объект заказчика.

        Returns:
            DetailedReplyDTO: DTO с подробными данными отклика или `None`, если отклик не найден.

        Raises:
            Exception: Если произошла ошибка при получении списка заказов.
        """
        pass
