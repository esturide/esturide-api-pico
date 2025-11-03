from pydantic import BaseModel


class GeoPoint(BaseModel):
    latitude: float
    longitude: float


class LocationModel(BaseModel):
    location: GeoPoint
    address: str
