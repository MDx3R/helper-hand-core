from typing import Literal, Optional

from pydantic import BaseModel


class ApplicationDTO(BaseModel):
    pass


class InternalDTO(ApplicationDTO):
    pass


class LastObjectDTO(InternalDTO):
    last_id: Optional[int] = None


class SortingDTO(InternalDTO):
    sorting: Literal["default", "ascending", "descending"] = "default"


class PaginationDTO(LastObjectDTO):
    size: int = (
        15  # TODO: Добавить ограничение по размеру? Такая проверка в контроллере
    )


class ContextDTO(InternalDTO):
    "Следует использовать только для создания производных DTO."

    pass
