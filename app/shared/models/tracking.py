from fireo.fields import IDField, DateTime, GeoPoint
from fireo.models import Model


class Tracking(Model):
    id = IDField()
    created = DateTime(auto=True)
    location = GeoPoint()
