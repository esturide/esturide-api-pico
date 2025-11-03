import datetime
from typing import List, Annotated

from beanie import Document, Link, Indexed
from pydantic import Field

from app.shared.models.tracking import Tracking
from app.shared.models.user import User
from app.shared.utils.random import generate_random_code_128


class RideTravelModel(Document):
    class Settings:
        name = "rides"

    code: Annotated[int, Indexed(unique=True)] = Field(default_factory=generate_random_code_128)
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

    @property
    def uuid(self):
        return self._id