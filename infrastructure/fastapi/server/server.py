from contextlib import asynccontextmanager
from functools import wraps
import inspect
from typing import Awaitable, Callable, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
        self._register_order_routers()
        self._register_reply_routers()
        print("Registered routes:", [route.path for route in self.app.routes])
        print("Done")

    def include_middlewares(self):
        from presentation.middleware.auth_middleware import (
            AuthMiddleware,
        )

        self.app.add_middleware(AuthMiddleware)
        self.include_cors_middleware()
        self.include_exception_handlers()

    def include_exception_handlers(self):
        pass

    def include_cors_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # TODO: Добавить в Config
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _register_auth_routers(self):
        from presentation.controllers.auth.auth import router as auth_router

        self.app.include_router(auth_router, prefix="/auth", tags=["Auth"])

    def _register_user_routers(self):
        from presentation.controllers.user.user_controller import (
            router as user_router,
            contractor_router as contractor_router,
            contractee_router as contractee_router,
            admin_router as admin_router,
        )

        self.app.include_router(
            user_router,
            prefix="/users",
            tags=["Users"],
        )

        self.app.include_router(
            contractor_router,
            prefix="/contractor/users",
            tags=["Contractor's Users"],
        )
        self.app.include_router(
            contractee_router,
            prefix="/contractee/users",
            tags=["Contractee's Users"],
        )
        self.app.include_router(
            admin_router, prefix="/admin/users", tags=["Admin's Users"]
        )

    def _register_order_routers(self):
        from presentation.controllers.order.order_contoller import (
            router as contractor_router,
            contractee_router as contractee_router,
            admin_router as admin_router,
        )

        self.app.include_router(
            contractor_router,
            prefix="/contractor/orders",
            tags=["Contractor's Orders"],
        )
        self.app.include_router(
            contractee_router,
            prefix="/contractee/orders",
            tags=["Contractee's Orders"],
        )
        self.app.include_router(
            admin_router,
            prefix="/admin/orders",
            tags=["Admin's Orders"],
        )

    def _register_reply_routers(self):
        from presentation.controllers.reply.contractee_reply_controller import (
            contractee_reply_router,
        )
        from presentation.controllers.reply.contractor_reply_controller import (
            contractor_reply_router,
        )

        self.app.include_router(
            contractor_reply_router,
            prefix="/contractor/replies",
            tags=["Contractor's Replies"],
        )
        self.app.include_router(
            contractee_reply_router,
            prefix="/contractee/replies",
            tags=["Contractee's Replies"],
        )
