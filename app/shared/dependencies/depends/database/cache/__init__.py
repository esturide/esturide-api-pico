import functools

import redis
import redis.asyncio

from app.core import get_settings


@functools.lru_cache
def get_async_cache():
    settings = get_settings()

    redis_client = redis.asyncio.Redis(
        host=settings.db_cache_host,
        port=settings.db_cache_port,
        decode_responses=True,
        username="default",
        password=settings.db_cache_password,
    )

    return redis_client


@functools.lru_cache
def get_cache():
    settings = get_settings()

    redis_client = redis.Redis(
        host=settings.db_cache_host,
        port=settings.db_cache_port,
        decode_responses=True,
        username="default",
        password=settings.db_cache_password,
    )

    return redis_client
