from fireo.fields import TextField, IDField, DateTime, ReferenceField, ListField, BooleanField, \
    NestedModel
from fireo.models import Model

from app.shared.models.tracking import TrackingRecord
from app.shared.models.user import User


class RideTravel(Model):
    class Meta:
        collection_name = "ride_travels"

    id = IDField()
    created = DateTime(auto=True)

    passenger = ReferenceField(User, required=True)

    seat = TextField(required=True)
    on_board = BooleanField(default=False, required=False)
    starting = DateTime(required=False)
    over = BooleanField(default=False)
    cancel = BooleanField(default=False)
    accept = BooleanField(default=False)

    tracking = ListField(ReferenceField(TrackingRecord), required=False)

    @property
    def is_finished(self):
        return self.over or self.cancel

    @property
    def is_current(self):
        return not self.over and not self.cancel
