import functools

import fireo
import fireo.database
import redis
import redis.asyncio

from app.core import get_settings


@functools.lru_cache
def get_async_cache() -> redis.asyncio.Redis:
    settings = get_settings()

    return redis.asyncio.Redis(
        host=settings.cache_host,
        port=settings.cache_port,
        decode_responses=True,
        username="default",
        password=settings.cache_password,
    )


@functools.lru_cache
def get_cache() -> redis.Redis:
    settings = get_settings()

    return redis.Redis(
        host=settings.cache_host,
        port=settings.cache_port,
        decode_responses=True,
        username="default",
        password=settings.cache_password,
    )


@functools.lru_cache
def get_document_db() -> fireo.database.Database:
    settings = get_settings()

    return fireo.connection(from_file=settings.db_credential)
