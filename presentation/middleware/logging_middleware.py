import logging
import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from dependency_injector.wiring import Provide, inject

from core.containers import Container


class LoggingMiddleware(BaseHTTPMiddleware):
    @inject
    def __init__(
        self,
        app,
        logger: logging.Logger = Provide[Container.logger],
    ):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Request logging
        self.logger.info(
            f"Incoming request: {request.method} {request.url.path}"
        )

        response: Response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = f"{process_time:.2f}ms"

        # Response logging
        self.logger.info(
            f"Completed response: {request.method} {request.url.path} "
            f"with status {response.status_code} in {formatted_process_time}"
        )

        return response
