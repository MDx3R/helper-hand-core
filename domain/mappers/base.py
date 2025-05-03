from typing import TypeVar
from domain.dto.base import ApplicationDTO
from domain.entities.base import ApplicationModel


E = TypeVar("T", bound=type[ApplicationModel])
D = TypeVar("T", bound=type[ApplicationDTO])


def from_entity_to_dto(entity: ApplicationModel, to: D, **kwargs) -> D:
    return to.model_validate(entity.model_dump() | kwargs)


def from_dto_to_entity(dto: ApplicationDTO, to: E, **kwargs) -> E:
    return to.model_validate(dto.model_dump() | kwargs)
