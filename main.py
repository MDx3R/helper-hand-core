from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from application.services.auth.user_auth_service import TokenService
from core.containers import Container
from domain.dto.user.base import UserCredentialsDTO
from domain.dto.user.internal.user_context_dto import UserContextDTO
from domain.dto.user.response.user_output_dto import AuthOutputDTO
from domain.entities.user.enums import RoleEnum, UserStatusEnum

# from presentation.controllers.auth.auth import get_current_user

app = FastAPI()

# Инициализация контейнера
container = Container()
container.init_resources()
# container.wire(modules=[__name__])  # Wire the container
# container.wire(modules=["presentation.controllers.auth.auth"])


def register_middleware(app: FastAPI):
    from presentation.middleware.auth_middleware import AuthMiddleware

    app.add_middleware(AuthMiddleware)


def register_routers(app: FastAPI, container: Container):
    from presentation.controllers.auth.auth import router as auth_router

    app.include_router(
        auth_router,
        prefix="/auth",
        tags=["Auth"],
    )
    register_user_routers(app)
    print(
        "Registered routes:",
        [route.path for route in app.routes],
    )
    print("Done")


def register_user_routers(app: FastAPI):
    from presentation.controllers.user.user_controller import (
        router as user_router,
        contractor_router as contractor_user_router,
        contractee_router as contractee_user_router,
        admin_router as admin_user_router,
    )

    # app.include_router(
    #     user_router,
    #     prefix="/users",
    #     tags=["Users"],
    # )
    app.include_router(
        contractor_user_router,
        prefix="/contractor/users",
        tags=["Contractor's Users"],
    )
    app.include_router(
        contractee_user_router,
        prefix="/contractee/users",
        tags=["Contractee's Users"],
    )
    app.include_router(
        admin_user_router,
        prefix="/admin/users",
        tags=["Admin's Users"],
    )


# @app.get("/")
# def hello(user: UserContextDTO = Depends(get_current_user)):
#     return f"Hello, {user.user_id}"


# @app.get("/token", response_model=AuthOutputDTO)
# @inject
# async def get_token(
#     service: TokenService = Depends(lambda: container.token_service()),
# ):
#     user_context = UserContextDTO(
#         user_id=1,
#         role=RoleEnum.admin,
#         status=UserStatusEnum.registered,
#         credentials=UserCredentialsDTO(telegram=None, web=None),
#     )
#     return await service.generate_token(user_context)


register_middleware(app)
register_routers(app, container)
