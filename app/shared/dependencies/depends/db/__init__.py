import functools

import fireo
import fireo.database
import redis
import redis.asyncio

from app.core import get_settings


@functools.lru_cache
def get_async_cache():
    settings = get_settings()

    redis_client = redis.asyncio.Redis(
        host=settings.cache_host,
        port=settings.cache_port,
        decode_responses=True,
        username="default",
        password=settings.cache_password,
    )

    return redis_client


@functools.lru_cache
def get_cache():
    settings = get_settings()

    redis_client = redis.Redis(
        host=settings.cache_host,
        port=settings.cache_port,
        decode_responses=True,
        username="default",
        password=settings.cache_password,
    )

    return redis_client


@functools.lru_cache
def get_document_db() -> fireo.database.Database:
    settings = get_settings()

    return fireo.connection(from_file=settings.db_credential)
