from typing import Optional
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