import datetime
import uuid
from typing import List, Annotated, Tuple

from beanie import Document, Indexed
from pydantic import Field, UUID4, BaseModel


class RecordPosition(BaseModel):
    created: datetime.datetime = Field(default_factory=datetime.datetime.now)

    latitude: float
    longitude: float


class Tracking(Document):
    class Settings:
        name = "tracking"

    uuid: Annotated[UUID4, Indexed(unique=True)] = Field(default_factory=uuid.uuid4)
    created: datetime.datetime = Field(default_factory=datetime.datetime.now)

    records: List[RecordPosition] = Field(default_factory=list)
