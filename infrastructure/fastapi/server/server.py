from contextlib import asynccontextmanager
from functools import wraps
import inspect
from typing import Awaitable, Callable, List
from fastapi import FastAPI


class FastAPIServer:
    def __init__(self):
        self._startup_handlers: List[Callable[[], Awaitable[None]]] = []
        self._shutdown_handlers: List[Callable[[], Awaitable[None]]] = []
        self.app = FastAPI(lifespan=self._lifespan)

    # TODO: Добавить приоритет
    def on_start_up(self, func: Callable, **kwargs):
        self._startup_handlers.append(self._wrap(func, **kwargs))

    def on_tear_down(self, func: Callable, **kwargs):
        self._shutdown_handlers.append(self._wrap(func, **kwargs))

    def _wrap(self, func: Callable, **kwargs) -> Callable[[], Awaitable[None]]:
        @wraps(func)
        async def wrapper():
            if inspect.iscoroutinefunction(func):
                await func(**kwargs)
            else:
                func(**kwargs)

        return wrapper

    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        try:
            for handler in self._startup_handlers:
                await handler()
            yield
        finally:
            for handler in reversed(self._shutdown_handlers):
                try:
                    await handler()
                except Exception as e:
                    print(f"Error in shutdown handler {handler.__name__}: {e}")

    def setup_routes(self):
        self._register_auth_routers()
        self._register_user_routers()
        print("Registered routes:", [route.path for route in self.app.routes])
        print("Done")

    def include_middlewares(self):
        from presentation.middleware.auth_middleware import (
            AuthMiddleware,
        )

        self.app.add_middleware(AuthMiddleware)

    def include_exception_handlers(self):
        pass

    def _register_auth_routers(self):
        from presentation.controllers.auth.auth import router as auth_router

        self.app.include_router(auth_router, prefix="/auth", tags=["Auth"])

    def _register_user_routers(self):
        from presentation.controllers.user.user_controller import (
            contractor_router as contractor_user_router,
            contractee_router as contractee_user_router,
            admin_router as admin_user_router,
        )

        self.app.include_router(
            contractor_user_router,
            prefix="/contractor/users",
            tags=["Contractor's Users"],
        )
        self.app.include_router(
            contractee_user_router,
            prefix="/contractee/users",
            tags=["Contractee's Users"],
        )
        self.app.include_router(
            admin_user_router, prefix="/admin/users", tags=["Admin's Users"]
        )
