import socketio

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    ping_interval=25,
    ping_timeout=20,
)

def mount_socketio(fastapi_app):
    return socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
