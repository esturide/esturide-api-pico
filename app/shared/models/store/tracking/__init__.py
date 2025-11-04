import uuid
from typing import List

from pydantic import UUID4
from aredis_om import JsonModel, Field

from app.shared.dependencies.depends.cache import get_async_client_redis
from app.shared.models.store import GeoLocationEmbedded


class TrackingStore(JsonModel):
    uuid: UUID4 = Field(default_factory=uuid.uuid4)

    position: List[GeoLocationEmbedded]

    class Meta:
        database = get_async_client_redis()
