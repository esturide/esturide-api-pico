import datetime
import uuid
from typing import List, Annotated, Optional, Set

from beanie import Document, Link, Indexed
from pydantic import Field, UUID4

from app.shared.const import DEFAULT_MAX_SCHEDULE_LIFETIME_HRS
from app.shared.models.ride import RideTravelModel
from app.shared.models.tracking import Tracking
from app.shared.models.user import User
from app.shared.types import SeatOption
from app.shared.types.enum import Gender


class ScheduleTravelModel(Document):
    class Settings:
        name = "schedules"

    uuid: Annotated[UUID4, Indexed(unique=True)] = Field(default_factory=uuid.uuid4)
    created: datetime.datetime = Field(default_factory=datetime.datetime.now)

    starting: Optional[datetime.datetime] = Field(None)
    terminated: Optional[datetime.datetime] = Field(None)

    terminate: bool = Field(False)
    cancel: bool = Field(False)

    driver: Link[User]
    rides: List[Link[RideTravelModel]] = Field([])

    price: int
    seats: Set[SeatOption] = Field({SeatOption.A, SeatOption.B, SeatOption.C})

    origin: str
    destination: str

    gender_filter: Set[Gender] = Field({Gender.male, Gender.female})

    waypoints: Set[str] = Field(default_factory=set)

    tracking: Link[Tracking] = Field(...)

    @property
    def is_enabled(self):
        return self.starting is not None and self.terminated is not None

    @property
    def is_started(self):
        return self.starting is not None

    @property
    def is_current(self):
        return not all([self.terminated, self.cancel])

    @property
    def is_finished(self):
        return self.terminated is not None

    @property
    def is_cancelled(self):
        return self.starting is not None and any([self.terminated, self.cancel])

    @property
    def is_active(self):
        return self.starting is not None and self.terminated is None and self.is_current

    @property
    def have_passengers(self):
        return self.rides is not None

    @property
    def seats_available(self):
        if isinstance(self.seats, list):
            return len(self.seats) != 0

        return False

    @property
    def lifetime_exceeded(self) -> bool:
        if not isinstance(self.starting, datetime.datetime):
            return False

        now = datetime.datetime.now(datetime.timezone.utc)
        eight_hours = datetime.timedelta(hours=DEFAULT_MAX_SCHEDULE_LIFETIME_HRS)

        return now > self.starting + eight_hours

    @property
    def accepted_genres(self) -> List[Gender]:
        if isinstance(self.gender_filter, list):
            return [Gender(gender) for gender in self.gender_filter]

        return []

    @property
    def max_passengers(self):
        return len(self.seats)
