from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class ApplicationModel(BaseModel):
    """
    Базовая модель всех моделей приложения.

    Представляет общие данные и логику для всех моделей.
    """

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_fields(self, *, exclude_none: bool = False) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            exclude={"created_at", "updated_at"},
            exclude_none=exclude_none,
        )
