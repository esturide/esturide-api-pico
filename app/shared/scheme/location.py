from pydantic import BaseModel, Field


class GeoLocationModel(BaseModel):
    longitude: float = Field(0, title="Longitude", alias='longitude')
    latitude: float = Field(0, title="Latitude", alias='latitude')
