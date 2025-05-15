from typing import TypeVar
from domain.dto.base import ApplicationDTO
from domain.entities.base import ApplicationModel


E = TypeVar("E", bound=ApplicationModel)
D = TypeVar("D", bound=ApplicationDTO)


def from_entity_to_dto(entity: ApplicationModel, to: type[D], **kwargs) -> D:
    return to.model_validate(entity.model_dump() | kwargs)


def from_dto_to_entity(dto: ApplicationDTO, to: type[E], **kwargs) -> E:
    return to.model_validate(dto.model_dump() | kwargs)
