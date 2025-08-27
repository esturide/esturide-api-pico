from pydantic import BaseModel, Field, field_validator


class GeoLocationModel(BaseModel):
    longitude: float = Field(0, title="Longitude", alias='longitude')
    latitude: float = Field(0, title="Latitude", alias='latitude')

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


class GeoLocationResultResponse(GeoLocationModel):
    address: str = Field("", alias='address')


class LocationAddressModel(BaseModel):
    address: str = Field("", alias='address')
