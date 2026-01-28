import functools

from fastsio import AsyncServer


@functools.lru_cache(maxsize=None)
def init_socketio_async_server():
    return AsyncServer(async_mode="asgi")
