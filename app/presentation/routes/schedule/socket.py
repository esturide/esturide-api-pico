import asyncio

from fastsio import SocketID, Auth, AsyncServer, RouterSIO, Depends

from app.shared.background.socketio import AsyncClientConnectionManager
from app.shared.dependencies.depends.socketio import get_async_client_manager

travel_sio = RouterSIO(namespace="/travel")


@travel_sio.event
async def connect(
        sid: SocketID,
        auth: Auth,
        server: AsyncServer,
        commons: AsyncClientConnectionManager = Depends(get_async_client_manager)
):
    print(f"Connection: {sid}, auth: {auth}")

    @commons.attach(sid)
    async def ping_message():
        while True:
            await server.emit("greetings", "Ping message", namespace="/travel", to=sid)
            await asyncio.sleep(1)

    return True


@travel_sio.event
async def disconnect(
        sid: SocketID,
        server: AsyncServer,
        commons: AsyncClientConnectionManager = Depends(get_async_client_manager)
):
    await commons.detach(sid)

    return True


@travel_sio.on("hello-world")
async def on_schedule(sid: SocketID, server: AsyncServer):
    await server.emit("greetings", "Hello world", namespace="/travel", to=sid)
