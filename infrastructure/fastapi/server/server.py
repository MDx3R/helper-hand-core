from contextlib import asynccontextmanager
from functools import wraps
import inspect
from typing import Awaitable, Callable, List
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.middleware.error_handling_middleware import (
    ErrorHandlingMiddleware,
)
from presentation.middleware.logging_middleware import LoggingMiddleware


class FastAPIServer:
    """
    Обертка сервера FastAPI.
    Обрабатывает регистрацию маршрутов, middleware и события жизненного цикла.
    """

    PREFIX = "api"
    ADMIN_BASE = "admin"
    CONTRACTOR_BASE = "contractor"
    CONTRACTEE_BASE = "contractee"
    USERS_BASE = "users"
    ORDERS_BASE = "orders"
    REPLIES_BASE = "replies"
    METRICS_BASE = "metrics"
    PHOTOS_BASE = "photos"

    def __init__(self):
        self._startup_handlers: List[Callable[[], Awaitable[None]]] = []
        self._shutdown_handlers: List[Callable[[], Awaitable[None]]] = []
        self.app = FastAPI(lifespan=self._lifespan)

    def on_start_up(self, func: Callable, **kwargs):
        """Регистрирует функцию для выполнения при запуске приложения."""
        self._startup_handlers.append(self._wrap(func, **kwargs))

    def on_tear_down(self, func: Callable, **kwargs):
        """Регистрирует функцию для выполнения при завершении работы приложения."""
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
        """Регистрирует все API-маршруты."""
        self._register_auth_routers()
        self._register_user_routers()
        self._register_order_routers()
        self._register_reply_routers()
        self._register_metrics_routers()
        self._register_photos_routers()
        route_paths = [
            getattr(route, "path", None)
            for route in self.app.routes
            if hasattr(route, "path")
        ]
        print("Registered routes:", route_paths)
        print("Done")

    def include_middlewares(self):
        """Регистрирует все middleware."""
        from presentation.middleware.auth_middleware import AuthMiddleware

        self._include_cors_middleware()
        self.app.add_middleware(LoggingMiddleware)
        self.app.add_middleware(ErrorHandlingMiddleware)
        self.app.add_middleware(AuthMiddleware)

    def include_exception_handlers(self):
        """Регистрирует все обработчики исключений."""
        pass

    def _include_cors_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # TODO: Добавь Config
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _register_auth_routers(self):
        from presentation.controllers.auth.auth import router as auth_router

        self._include_router(auth_router, "auth", "Auth")

    def _register_user_routers(self):
        from presentation.controllers.user.user_controller import (
            router as user_router,
            contractor_router,
            contractee_router,
            admin_router,
        )

        self._include_router(user_router, f"{self.USERS_BASE}", "Users")
        self._include_router(
            contractor_router,
            f"{self.CONTRACTOR_BASE}/{self.USERS_BASE}",
            "Contractor's Users",
        )
        self._include_router(
            contractee_router,
            f"{self.CONTRACTEE_BASE}/{self.USERS_BASE}",
            "Contractee's Users",
        )
        self._include_router(
            admin_router,
            f"{self.ADMIN_BASE}/{self.USERS_BASE}",
            "Admin's Users",
        )

    def _register_order_routers(self):
        from presentation.controllers.order.order_contoller import (
            guest_router,
            contractor_router,
            contractee_router,
            admin_router,
        )

        self._include_router(guest_router, f"{self.ORDERS_BASE}", "Orders")
        self._include_router(
            contractor_router,
            f"{self.CONTRACTOR_BASE}/{self.ORDERS_BASE}",
            "Contractor's Orders",
        )
        self._include_router(
            contractee_router,
            f"{self.CONTRACTEE_BASE}/{self.ORDERS_BASE}",
            "Contractee's Orders",
        )
        self._include_router(
            admin_router,
            f"{self.ADMIN_BASE}/{self.ORDERS_BASE}",
            "Admin's Orders",
        )

    def _register_reply_routers(self):
        from presentation.controllers.reply.contractee_reply_controller import (
            contractee_reply_router,
        )
        from presentation.controllers.reply.contractor_reply_controller import (
            contractor_reply_router,
        )

        self._include_router(
            contractor_reply_router,
            f"{self.CONTRACTOR_BASE}/{self.REPLIES_BASE}",
            "Contractor's Replies",
        )
        self._include_router(
            contractee_reply_router,
            f"{self.CONTRACTEE_BASE}/{self.REPLIES_BASE}",
            "Contractee's Replies",
        )

    def _register_metrics_routers(self):
        from presentation.controllers.metrics.metrics_controller import (
            app_router,
            contractor_router,
            contractee_router,
            admin_router,
        )

        self._include_router(app_router, f"{self.METRICS_BASE}", "Orders")
        self._include_router(
            contractor_router,
            f"{self.CONTRACTOR_BASE}/{self.METRICS_BASE}",
            "Contractor's Metrics",
        )
        self._include_router(
            contractee_router,
            f"{self.CONTRACTEE_BASE}/{self.METRICS_BASE}",
            "Contractee's Metrics",
        )
        self._include_router(
            admin_router,
            f"{self.ADMIN_BASE}/{self.METRICS_BASE}",
            "Admin's Metrics",
        )

    def _register_photos_routers(self):
        from presentation.controllers.photo_controller import router

        self._include_router(router, f"{self.PHOTOS_BASE}", "Photos")

    def _include_router(self, router: APIRouter, prefix: str, tag: str):
        prefix = f"/{self.PREFIX}/{prefix}" if self.PREFIX else f"/{prefix}"
        self.app.include_router(router, prefix=prefix, tags=[tag])
