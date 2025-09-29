import functools

from redis import Redis

from app.core import get_settings


@functools.lru_cache
def get_cache():
    settings = get_settings()

    return Redis(
        host=settings.cache_host,
        port=settings.cache_port,
        decode_responses=True,
        username="default",
        password=settings.cache_password,
    )
