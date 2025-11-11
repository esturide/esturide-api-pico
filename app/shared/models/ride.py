import datetime
import uuid
from typing import Annotated

from beanie import Document, Link, Indexed
from pydantic import Field, UUID4

from app.shared.models.tracking import Tracking
from app.shared.models.user import UserDocument
from app.shared.types import Seat


class RideTravelModel(Document):
    class Settings:
        name = "rides"

    uuid: Annotated[UUID4, Indexed(unique=True)] = Field(default_factory=uuid.uuid4)
    created: datetime.datetime = Field(default_factory=datetime.datetime.now)

    passenger: Link[UserDocument]

    seat: Seat
    on_board: bool
    starting: bool
    over: bool
    cancel: bool
    accept: bool

    tracking: Link[Tracking] = Field(default_factory=Tracking)

    @property
    def is_finished(self):
        return self.over or self.cancel

    @property
    def is_current(self):
        return not self.over and not self.cancel
