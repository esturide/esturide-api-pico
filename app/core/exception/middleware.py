from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.shared.scheme import StatusMessage
from app.shared.types.enum import Status


class ModelResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except RequestValidationError as exc:
            error_response = StatusMessage(
                status=Status.failure,
                message="Signature verification failed."
            )

            return JSONResponse(
                status_code=422,
                content=error_response.model_dump(),
            )
