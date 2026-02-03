from fastapi.responses import JSONResponse

from app.shared.dependencies.depends import get_logger
from app.shared.scheme import StatusMessage
from app.shared.types.enum import Status


async def not_implemented_handler(request, exc):
    logger = get_logger()

    error_response = StatusMessage(
        status=Status.failure,
        message="The requested method is not currently available on this server."
    )

    logger.warning(f"Method not implemented in {request.url.path}: {str(exc)}")

    return JSONResponse(status_code=501, content=error_response.model_dump())

async def custom_http_exception_handler(request, exc):
    logger = get_logger()

    error_response = StatusMessage(
        status=Status.failure,
        message=str(exc.detail)
    )

    logger.error(f"Exception details: {exc.detail}")

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
    logger = get_logger()

    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )


async def validation_exception_handler(request, exc):
    logger = get_logger()
    errors = exc.errors()
    error_messages = []

    for error in errors:
        error_messages.append(error.get_from_user('msg', 'Error message not available.'))

    body = await request.body()

    logger.error(exc.errors())
    logger.error(f"Validation error: {exc}")
    logger.error(f"JSON received that failed: {body.decode('utf-8')}")

    return JSONResponse(
        status_code=422,
        content={"message": "Validation error.", "details": error_messages},
    )


async def database_exception_handler(request, exc):
    logger = get_logger()
    error_response = StatusMessage(
        status=Status.failure,
        message="Error in database query."
    )

    return JSONResponse(status_code=500, content=error_response.model_dump())
