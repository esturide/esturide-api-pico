from fireo.fields import TextField, IDField, DateTime, NumberField, ReferenceField, GeoPoint, ListField, BooleanField, \
    NestedModel
from fireo.models import Model

from app.shared.models.ride import RideTravel
from app.shared.models.tracking import Tracking
from app.shared.models.user import User


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
    passengers = ListField(ReferenceField(RideTravel), required=False)
    max_passengers = NumberField(default=3)

    origin = GeoPoint(required=True)
    destination = GeoPoint(required=True)
    price = NumberField(required=True)
    seats = ListField(TextField(), required=True)

    tracking = ListField(NestedModel(Tracking), required=False)

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
        return self.passengers is not None
