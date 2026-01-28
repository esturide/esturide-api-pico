from fastsio import SocketID, Environ, Auth, Data

from app.shared.dependencies.depends.socketio import init_socketio_async_server

sio = init_socketio_async_server()

@sio.event
async def connect(
    sid: SocketID,
    environ: Environ,
    auth: Auth,
):
    print(f"Client {sid} connected")
    return True


@sio.event
async def disconnect(sid: SocketID):
    print(f"Client {sid} disconnected")


@sio.on("message")
async def handle_message(sid: SocketID, data: Data):
    await sio.emit("response", f"Received: {data}", to=sid)
