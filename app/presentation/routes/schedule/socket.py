import asyncio

from fastsio import SocketID, Auth, AsyncServer, RouterSIO, Depends

from app.application.usecase.auth import get_auth_session_case, AuthSessionUseCase
from app.shared.background.socketio import AsyncClientConnectionManager
from app.shared.dependencies.depends.socketio import get_async_client_manager
from app.shared.events import AsyncSocketEmitter

travel_sio = RouterSIO(namespace="/travel")


@travel_sio.event
async def connect(
        sid: SocketID,
        auth: Auth,
        server: AsyncServer,
        auth_session: AuthSessionUseCase = Depends(get_auth_session_case),
        commons: AsyncClientConnectionManager = Depends(get_async_client_manager)
):
    token = auth["token"]

    if not await auth_session.check(token):
        return False

    emitter = AsyncSocketEmitter(server, namespace="/travel", sid=sid)

    @commons.attach(sid)
    async def ping_message():
        while True:
            await emitter.send(
                "ping",
                "It's working!"
            )

            await asyncio.sleep(5)

    return True


@travel_sio.event
async def disconnect(
        sid: SocketID,
        commons: AsyncClientConnectionManager = Depends(get_async_client_manager)
):
    await commons.detach(sid)

    return True


@travel_sio.on("schedule")
async def on_schedule(
        sid: SocketID,
        server: AsyncServer,
        commons: AsyncClientConnectionManager = Depends(get_async_client_manager)
):
    pass
