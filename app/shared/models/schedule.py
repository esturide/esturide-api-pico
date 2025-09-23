import datetime
from typing import List

from fireo.fields import TextField, IDField, DateTime, NumberField, ReferenceField, ListField, BooleanField, \
    NestedModel
from fireo.models import Model

from app.shared.const import DEFAULT_MAX_SCHEDULE_LIFETIME_HRS
from app.shared.models.location import LocationModel
from app.shared.models.ride import RideTravel
from app.shared.models.tracking import TrackingRecord
from app.shared.models.user import User
from app.shared.types.enum import Gender


class ScheduleTravel(Model):
    class Meta:
        collection_name = "schedule_travels"

    id = IDField()
    created = DateTime(auto=True)

    starting = DateTime(required=False)
    terminated = DateTime(required=False)

    terminate = BooleanField(default=False)
    cancel = BooleanField(default=False)

    driver = ReferenceField(User, required=True)
    rides = ListField(ReferenceField(RideTravel), required=False)
    max_passengers = NumberField(default=3)

    price = NumberField(required=True)
    seats = ListField(TextField(), required=True)

    origin = NestedModel(LocationModel, required=True)
    destination = NestedModel(LocationModel, required=True)

    gender_filter = ListField(TextField(), required=True)

    tracking = ListField(NestedModel(TrackingRecord), required=False)

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

        now = datetime.datetime.now()
        time_difference = now - self.starting
        eight_hours = datetime.timedelta(hours=DEFAULT_MAX_SCHEDULE_LIFETIME_HRS)

        return time_difference > eight_hours

    @property
    def accepted_genres(self) -> List[Gender]:
        if isinstance(self.gender_filter, list):
            return [Gender(gender) for gender in self.gender_filter]

        return []
