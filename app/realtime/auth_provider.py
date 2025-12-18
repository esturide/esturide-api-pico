import socketio

from app.realtime.namespaces.driver import DriverNamespace

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    ping_interval=25,
    ping_timeout=20,
)

sio.register_namespace(DriverNamespace("/driver"))


def mount_socketio(fastapi_app):
    # ASGI final: Socket.IO + FastAPI
    return socketio.ASGIApp(sio, other_asgi_app=fastapi_app)
