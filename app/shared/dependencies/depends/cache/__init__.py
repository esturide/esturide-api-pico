import functools

import redis
import redis.asyncio as aioredis

from app.core import get_settings

@functools.lru_cache
def get_async_client_redis() -> aioredis.Redis:
    settings = get_settings()
    cache_host = settings.cache_host
    cache_port = settings.cache_port
    cache_password = settings.cache_password

    return aioredis.Redis(
        host=cache_host,
        password=cache_password,
        port=cache_port,
        decode_responses=True,
        username="default",
    )


@functools.lru_cache
def get_client_redis() -> redis.Redis:
    settings = get_settings()
    cache_host = settings.cache_host
    cache_port = settings.cache_port
    cache_password = settings.cache_password

    return redis.Redis(
        host=cache_host,
        password=cache_password,
        port=cache_port,
        decode_responses=True,
        username="default",
    )
