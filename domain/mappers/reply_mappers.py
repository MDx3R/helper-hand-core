from domain.dto.reply.request.create_reply_dto import CreateReplyDTO
from domain.dto.reply.request.reply_input_dto import ReplyInputDTO
from domain.dto.reply.response.reply_output_dto import (
    CompleteReplyOutputDTO,
    ReplyOutputDTO,
)
from domain.entities.reply.composite_reply import CompleteReply
from domain.entities.reply.reply import Reply
from domain.mappers.base import from_dto_to_entity, from_entity_to_dto


class ReplyMapper:
    @staticmethod
    def to_output(reply: Reply) -> ReplyOutputDTO:
        return from_entity_to_dto(reply, ReplyOutputDTO)

    @staticmethod
    def to_complete(reply: CompleteReply) -> CompleteReplyOutputDTO:
        return from_entity_to_dto(reply, CompleteReplyOutputDTO)

    @staticmethod
    def from_input(reply: ReplyInputDTO, wager: int) -> Reply:
        return from_dto_to_entity(reply, Reply, wager=wager)

    @staticmethod
    def from_create(
        reply: CreateReplyDTO, contractee_id: int, wager: int
    ) -> Reply:
        return from_dto_to_entity(
            reply, Reply, contractee_id=contractee_id, wager=wager
        )
