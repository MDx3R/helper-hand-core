from pydantic import BaseModel

from domain.entities.base import ApplicationModel

class ApplicationDTO(BaseModel):
    @classmethod
    def from_model(cls, model: ApplicationModel) -> 'ApplicationDTO':
        return cls.model_validate(model.get_fields())