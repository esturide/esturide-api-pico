import functools

from pymongo import AsyncMongoClient, MongoClient

from app.core import get_settings


@functools.lru_cache
def async_client_mongodb() -> AsyncMongoClient:
    settings = get_settings()

    return AsyncMongoClient(settings.mongodb_uri)


@functools.lru_cache
def client_mongodb() -> MongoClient:
    settings = get_settings()

    return MongoClient(settings.mongodb_uri)
