import functools

from fastsio import AsyncServer

from app.core import get_settings
from app.shared.background.socketio import AsyncClientConnectionManager


@functools.lru_cache
def get_root_socketio_server() -> AsyncServer:
    settings = get_settings()

    return AsyncServer(
        async_mode="asgi",
        logger=True,
        engineio_logger=True,
        cors_allowed_origins=settings.allowed_cors
    )


@functools.lru_cache
async def get_async_client_manager() -> AsyncClientConnectionManager:
    return AsyncClientConnectionManager()
