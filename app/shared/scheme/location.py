from pydantic import BaseModel, Field, field_validator


class GeoPoint(BaseModel):
    longitude: float = Field(..., title="Longitude", alias='longitude')
    latitude: float = Field(..., title="Latitude", alias='latitude')

    def __iter__(self):
        return iter([self.longitude, self.latitude])

    @field_validator('longitude')
    def check_longitude(cls, longitude):
        if -180 <= longitude <= 180:
            return longitude

        raise ValueError('Invalid longitude.')

    @field_validator('latitude')
    def check_latitude(cls, latitude):
        if -90 <= latitude <= 90:
            return latitude

        raise ValueError('Invalid latitude.')


class LocationAddressModel(BaseModel):
    address: str = Field("", alias='address')


class GeoLocationAddressModel(GeoPoint):
    address: str = Field("", alias='address')
