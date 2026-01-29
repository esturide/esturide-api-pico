import functools

from fastsio import AsyncServer


@functools.lru_cache(maxsize=None)
def get_root_socketio_server():
    return AsyncServer(async_mode="asgi", logger=True, engineio_logger=True)
