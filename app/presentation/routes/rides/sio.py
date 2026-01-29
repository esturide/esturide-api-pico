from fastsio import SocketID, Environ, Auth, Data, AsyncServer, RouterSIO
from pydantic import BaseModel


sio_ride = RouterSIO()

class Message(BaseModel):
    text: str
    room: str


class JoinRoom(BaseModel):
    room: str


@sio_ride.on("connect")
async def on_connect(
    sid: SocketID,
    environ: Environ,
    auth: Auth,
    server: AsyncServer
):
    print(f"Connection: {sid}, auth: {auth}")
    return True


@sio_ride.on("join_room")
async def on_join_room(
    sid: SocketID,
    server: AsyncServer, 
    data: JoinRoom  # Automatic Pydantic validation
):
    await server.enter_room(sid, data.room)
    await server.emit("joined", {"room": data.room}, to=sid)


@sio_ride.on("send_message")
async def on_send_message(
    sid: SocketID,
    server: AsyncServer,
    data: Message
):
    await server.emit(
        "new_message",
        data.model_dump(),
        room=data.room
    )
