import asyncio

from fastsio import SocketID, Environ, Auth, AsyncServer, RouterSIO

travel_sio = RouterSIO(namespace="/travel")


@travel_sio.on("connect")
async def on_connect(
        sid: SocketID,
        environ: Environ,
        auth: Auth,
        server: AsyncServer
):
    print(f"Connection: {sid}, auth: {auth}")
    return True


@travel_sio.on("hello-world")
async def on_schedule(sid: SocketID, environ: Environ, server: AsyncServer):
    await server.emit("greetings", "Hello world", namespace="/travel", to=sid)

    return True
