from fireo.fields import TextField, IDField, DateTime, NumberField, ReferenceField, GeoPoint, ListField, BooleanField
from fireo.models import Model


class Tracking(Model):
    id = IDField()
    created = DateTime(auto=True)
    location = GeoPoint()
