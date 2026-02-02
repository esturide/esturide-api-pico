import asyncio
import functools

from fastsio import SocketID, Environ, Auth, AsyncServer, RouterSIO, Depends

from app.shared.pattern.singleton import Singleton

travel_sio = RouterSIO(namespace="/travel")

class AsyncClientConnectionManager(metaclass=Singleton):
    def __init__(self):
        self.__sid = {}

    def attach(self, sid: str):
        def inner(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                await func(*args, **kwargs)

            task = asyncio.create_task(wrapper())
            self.__sid[sid] = task

            return task

        return inner

    async def detach(self, sid: str):
        if sid in self.__sid and not self.__sid[sid].done():
            self.__sid[sid].cancel()

            await self.__sid[sid]

        return None


async def get_async_client_manager() -> AsyncClientConnectionManager:
    return AsyncClientConnectionManager()


@travel_sio.event
async def connect(
        sid: SocketID,
        environ: Environ,
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
        environ: Environ,
        server: AsyncServer,
        commons: AsyncClientConnectionManager = Depends(get_async_client_manager)
):
    await commons.detach(sid)

    return True


@travel_sio.on("hello-world")
async def on_schedule(sid: SocketID, environ: Environ, server: AsyncServer):
    await server.emit("greetings", "Hello world", namespace="/travel", to=sid)
