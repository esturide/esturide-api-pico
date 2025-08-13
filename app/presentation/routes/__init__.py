from fastapi import APIRouter
from fastapi_sse import sse_handler

from app.shared.scheme import StatusSuccess, StatusMessage

root_router = APIRouter(
    tags=["Root router"]
)


@root_router.get("/")
async def endpoint_status():
    return StatusSuccess()


@root_router.get("/stream", response_model=StatusMessage)
@sse_handler()
async def message_generator(some_url_arg: str, repeat: int = 5):
    for i in range(repeat):
        yield StatusSuccess(message=f"Hello, {some_url_arg}!")

    yield StatusSuccess(message="Another message")
