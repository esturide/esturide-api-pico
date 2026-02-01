import datetime

from aredis_om import JsonModel, Field, EmbeddedJsonModel

from app.shared.dependencies.depends.cache import get_async_client_redis
from app.shared.types import Seat, Gender


class DesignatedDriver(EmbeddedJsonModel):
    usercode: int = Field(..., index=True)
    accepted: bool = Field(False, index=True)


class RideStore(JsonModel):
    usercode: int = Field(..., index=True, const=True)
    created: datetime.datetime = Field(default_factory=datetime.datetime.now, index=True, const=True)

    origin: str = Field(..., index=True, const=True)
    destination: str = Field(..., index=True, const=True)

    gender: Gender = Field(..., const=True)
    set: Seat = Field(..., const=True)

    drivers: DesignatedDriver = Field(...)

    class Meta:
        database = get_async_client_redis()
