import datetime
from typing import List

from beanie import Document, Link
from pydantic import Field

from app.shared.models.tracking import Tracking
from app.shared.models.user import User


class RideTravel(Document):
    class Settings:
        name = "rides"

    created: datetime.datetime = Field(default_factory=datetime.datetime.now)

    passenger: Link[User]

    seat: str
    on_board: bool
    starting: bool
    over: bool
    cancel: bool
    accept: bool

    tracking: List[Link[Tracking]]

    @property
    def is_finished(self):
        return self.over or self.cancel

    @property
    def is_current(self):
        return not self.over and not self.cancel
