import logging
from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from core.containers import Container
from domain.exceptions.base import (
    RepositoryException,
    ServiceException,
)

from dependency_injector.wiring import Provide, inject


class ExceptionHandler:
    def __init__(self):
        self._handlers = {}

        # Регистрация обработчиков исключений
        self.register(ServiceException, self._handle_service_exception)
        self.register(RepositoryException, self._handle_internal_error)
        self.register(Exception, self._handle_internal_error)

    def register(self, exc_type, handler):
        self._handlers[exc_type] = handler

    def handle(self, exc: Exception) -> str:
        for exc_type, handler in self._handlers.items():
            if isinstance(exc, exc_type):
                return handler(exc)
        return self._handle_internal_error(exc)

    def _handle_service_exception(self, exc: Exception) -> str:
        return str(exc)

    def _handle_internal_error(self, exc: Exception) -> str:
        return "Internal Error"


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    @inject
    def __init__(
        self,
        app,
        logger: logging.Logger = Provide[Container.logger],
        exception_handler: ExceptionHandler | None = None,
    ):
        super().__init__(app)
        self.logger = logger
        self.exception_handler = exception_handler or ExceptionHandler()

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            return response
        except (RequestValidationError, ValidationError) as validation_exc:
            self.logger.info(f"Validation error: {validation_exc}")
            return JSONResponse(
                status_code=422,
                content={
                    "error": "ValidationError",
                    "message": "Validation failed",
                    "details": (
                        validation_exc.errors()
                        if hasattr(validation_exc, "errors")
                        else str(validation_exc)
                    ),
                },
            )
        except Exception as exc:
            self.logger.exception("Unhandled exception")
            message = self.exception_handler.handle(exc)

            return JSONResponse(
                content={"error": message},
                status_code=400 if isinstance(exc, ServiceException) else 500,
            )
