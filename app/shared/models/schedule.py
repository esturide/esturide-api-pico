import datetime
from typing import List

from beanie import Document, Link
from pydantic import Field

from app.shared.const import DEFAULT_MAX_SCHEDULE_LIFETIME_HRS
from app.shared.models.location import LocationModel
from app.shared.models.ride import RideTravel
from app.shared.models.tracking import Tracking
from app.shared.models.user import User
from app.shared.types.enum import Gender


class ScheduleTravel(Document):
    class Settings:
        name = "schedules"

    created: datetime.datetime = Field(default_factory=datetime.datetime.now)

    starting: datetime.datetime
    terminated: datetime.datetime

    terminate: bool
    cancel: bool

    drive: Link[User]
    rides: List[Link[RideTravel]]
    max_passengers: int

    price: float
    seats: List[str]

    origin: LocationModel
    destination: LocationModel

    gender_filter: List[str]

    waypoints: List[LocationModel]

    tracking: List[Link[Tracking]]

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
