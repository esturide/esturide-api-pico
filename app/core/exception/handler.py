from fastapi.responses import JSONResponse

from app.shared.scheme import StatusMessage
from app.shared.types.enum import Status


async def custom_http_exception_handler(request, exc):
    error_response = StatusMessage(
        status=Status.failure,
        message=str(exc.detail)
    )

    return JSONResponse(status_code=exc.status_code, content=error_response.model_dump())


async def http_exception_handler(request, exc):
    if exc.status_code in [400, 401, 403, 404, 406, 422]:
        error_response = StatusMessage(
            status=Status.failure,
            message=str(exc.detail)
        )

        return JSONResponse(status_code=exc.status_code, content=error_response.model_dump())

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


async def invalid_credentials_handler(request, exc):
    error_response = StatusMessage(
        status=Status.failure,
        message="Signature verification failed."
    )

    return JSONResponse(status_code=401, content=error_response.model_dump())


async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )


async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "details": exc.errors()},
    )
