from domain.dto.user.internal.user_context_dto import WithUserContextDTO


class RemovePhotoDTO(WithUserContextDTO):
    photo_id: str
