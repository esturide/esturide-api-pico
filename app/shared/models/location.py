from fireo.fields import IDField, GeoPoint, TextField
from fireo.models import Model


class LocationModel(Model):
    class Meta:
        collection_name = "location_model"

    id = IDField()

    location = GeoPoint(required=True)
    address = TextField(required=True)
