import datetime

from aredis_om import HashModel, Field

from app.shared.dependencies.depends.cache import get_async_client_redis


class TrackingStore(HashModel):
    usercode: int = Field(index=True, const=True)

    record: datetime.datetime = Field(default_factory=datetime.datetime.now, const=True)

    latitude: float = Field(const=True)
    longitude: float = Field(const=True)

    class Meta:
        database = get_async_client_redis()
