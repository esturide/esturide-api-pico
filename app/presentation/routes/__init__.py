from fastapi import APIRouter

from app.shared.scheme import StatusSuccess, StatusMessage

root_router = APIRouter(
    tags=["Root router"]
)


@root_router.get("/")
async def endpoint_status() -> StatusMessage:
    return StatusSuccess(message="The API is working correctly!")
