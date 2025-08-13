from fireo.fields import IDField, DateTime, GeoPoint
from fireo.models import Model


class TrackingRecord(Model):
    class Meta:
        collection_name = "tracking_record"

    id = IDField()
    created = DateTime(auto=True)
    location = GeoPoint()
