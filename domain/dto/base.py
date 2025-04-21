from typing import Optional

from pydantic import BaseModel


class ApplicationDTO(BaseModel):
    pass


class InternalDTO(ApplicationDTO):
    pass


class LastObjectDTO(InternalDTO):
    last_id: Optional[int] = None


class PaginationDTO(LastObjectDTO):
    size: int = 15  # TODO: Добавить ограничение по размеру


class ContextDTO(InternalDTO):
    "Следует использовать только для создания производных DTO."

    pass
