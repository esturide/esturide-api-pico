from fastsio import SocketID, Environ, Auth, Data, AsyncServer, RouterSIO
from pydantic import BaseModel


ride_sio = RouterSIO(namespace="/ride")

class Message(BaseModel):
    text: str
    room: str


class JoinRoom(BaseModel):
    room: str


@ride_sio.on("connect")
async def on_connect(
    sid: SocketID,
    environ: Environ,
    auth: Auth,
    server: AsyncServer
):
    print(f"Connection: {sid}, auth: {auth}")
    return True


@ride_sio.on("send_message")
async def on_send_message(
    sid: SocketID,
    server: AsyncServer,
    data: Message
):
    await server.emit(
        "new_message",
        data.model_dump(),
        namespace="/ride"
    )
