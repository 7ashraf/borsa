from __future__ import annotations
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: object) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        response: Response = await call_next(request)  # type: ignore[arg-type, operator]
        response.headers["X-Request-ID"] = request_id
        return response
