import functools

from fastsio import AsyncServer


@functools.lru_cache
def get_root_socketio_server() -> AsyncServer:
    return AsyncServer(async_mode="asgi", logger=True, engineio_logger=True)
