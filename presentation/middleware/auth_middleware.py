from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from presentation.controllers.permissions import get_claims_from_token


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = self._extract_token(request)

        claims = None
        if token:
            try:
                claims = await get_claims_from_token(token)
            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code,
                    content={"detail": e.detail},
                )

        request.state.claims = claims
        response = await call_next(request)
        return response

    def _extract_token(self, request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[len("Bearer ") :]
        return ""
