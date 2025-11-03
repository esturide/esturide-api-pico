import datetime

from beanie import Document
from pydantic import Field

from app.shared.models.location import GeoPoint


class Tracking(Document):
    class Settings:
        name = "tracking"

    created: datetime.datetime = Field(default_factory=datetime.datetime.now)
    location: GeoPoint
