import functools

import aredis_om
import redis
import redis.asyncio as aioredis
import redis_om

from app.core import get_settings


@functools.lru_cache
def get_async_client_redis() -> aioredis.Redis:
    settings = get_settings()
    cache_host = settings.cache_host
    cache_port = settings.cache_port
    cache_password = settings.cache_password

    return aredis_om.get_redis_connection(
        host=cache_host,
        port=cache_port,
        decode_responses=True,
        username="default",
        password=cache_password
    )


@functools.lru_cache
def get_client_redis() -> redis.Redis:
    settings = get_settings()
    cache_host = settings.cache_host
    cache_port = settings.cache_port
    cache_password = settings.cache_password

    return redis_om.get_redis_connection(
        host=cache_host,
        port=cache_port,
        decode_responses=True,
        username="default",
        password=cache_password
    )
