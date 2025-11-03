from pydantic import BaseModel

from app.shared.scheme.location import GeoPoint


class LocationModel(BaseModel):
    location: GeoPoint
    address: str

    def __hash__(self):
        return hash(self.address)
