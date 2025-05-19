from application.usecases.reply.reply_query_use_case import GetReplyUseCase
from domain.dto.reply.internal.reply_query_dto import GetReplyDTO
from domain.dto.reply.response.reply_output_dto import CompleteReplyOutputDTO


class GetReplyForContracteeUseCase(GetReplyUseCase):
    async def execute(
        self, query: GetReplyDTO
    ) -> CompleteReplyOutputDTO | None:
        # Следует оставить здесь, так как подобна проверка в этом контексте выглядит уместо.
        # Например, также проверяется принадлежность заказа заказчику.
        # TODO: Перенести в Domain-сервис.
        if query.contractee_id != query.context.user_id:
            return None
        return await super().execute(query)
