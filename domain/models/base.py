from typing import Optional, Any
from pydantic import BaseModel

from datetime import datetime

class ApplicationModel(BaseModel):
    """
    Базовая модель всех моделей приложения.

    Представляет общие данные и логику для всех моделей.
    """

    created_at: Optional[datetime] = None
    """Дата создания сущности"""

    updated_at: Optional[datetime] = None
    """Дата создания сущности"""

    def get_fields(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True)