from fireo.fields import TextField, IDField, DateTime, NumberField, ReferenceField, GeoPoint, ListField, BooleanField, \
    NestedModel
from fireo.models import Model

from app.shared.models.tracking import Tracking
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

    tracking = ListField(NestedModel(Tracking), required=False)

    @property
    def is_finished(self):
        return self.over or self.cancel

    @property
    def is_current(self):
        return not self.over and not self.cancel
