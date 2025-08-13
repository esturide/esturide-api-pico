import typing

from fastapi import APIRouter, Cookie
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket

from app.shared.scheme import StatusSuccess

root_router = APIRouter(
    tags=["Root router"]
)


@root_router.get("/")
async def endpoint_status():
    return StatusSuccess()


@root_router.get("/cookie")
async def read_items(ads_id: typing.Annotated[str | None, Cookie()] = None):
    return {
        "ads_id": ads_id
    }


@root_router.post("/cookie")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}

    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")

    return response


@root_router.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"msg": "Hello WebSocket"})
    await websocket.close()
