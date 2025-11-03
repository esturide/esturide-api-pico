import datetime
from typing import List, Set

from aredis_om import JsonModel, Field
from pydantic import UUID4

from app.shared.dependencies.depends.cache import get_async_client_redis
from app.shared.models.store import GeoLocationEmbedded


class ScheduleTravelCache(JsonModel):
    travel_uuid: UUID4 = Field(index=True)
    origin: str = Field(index=True)
    destination: str = Field(index=True)

    starting: datetime.datetime = Field(index=True, sortable=True)

    waypoints: Set[str] = Field(default_factory=set)
    route: List[GeoLocationEmbedded] = Field(default_factory=list)

    class Meta:
        database = get_async_client_redis()
