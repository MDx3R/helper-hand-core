from typing import BinaryIO
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Response,
    UploadFile,
)
from fastapi.responses import StreamingResponse
from core.containers import Container
from dependency_injector.wiring import Provide, inject
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.request.upload_photo_dto import RemovePhotoDTO
from domain.dto.user.response.user_output_dto import UserOutputDTO
from fastapi_utils.cbv import cbv

from domain.services.user_photo_service import PhotoService
from presentation.controllers.permissions import (
    authenticated,
)


router = APIRouter(dependencies=[Depends(authenticated)])


@inject
def photo_service_factory(
    service: PhotoService = Depends(Provide[Container.photo_service]),
):
    return service


@cbv(router)
class UserPhotoController:
    ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
    photo_service: PhotoService = Depends(photo_service_factory)

    @router.post("/", response_model=UserOutputDTO)
    async def upload_photo(
        self,
        file: UploadFile = File(...),
        user: UserContextDTO = Depends(authenticated),
    ):
        if file.content_type not in self.ALLOWED_CONTENT_TYPES:
            raise HTTPException(
                status_code=400, detail="Недопустимый тип файла"
            )

        return await self.photo_service.upload_photo(file.file, context=user)

    @router.get("/{photo_id}", response_class=StreamingResponse)
    async def get_photo(self, photo_id: str):
        stream = await self.photo_service.get_photo(photo_id)
        return self._to_response(stream)

    @router.delete("/{photo_id}", response_model=UserOutputDTO)
    async def remove_photo(
        self,
        photo_id: str,
        user: UserContextDTO = Depends(authenticated),
    ):
        return await self.photo_service.remove_photo(
            RemovePhotoDTO(photo_id=photo_id, context=user)
        )

    def _to_response(self, stream: BinaryIO) -> Response:
        return StreamingResponse(stream, media_type="image/jpeg")
