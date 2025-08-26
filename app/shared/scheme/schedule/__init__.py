from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from app.shared.const import DEFAULT_PRICE, DEFAULT_MIN_PRICE
from app.shared.scheme.location import GeoLocationModel
from app.shared.types import UUID
from app.shared.types.enum.default_location import DefaultLocation, DEFAULT_LOCATION, get_gps_from_location


class CurrentUser(BaseModel):
    code: int
    first_name: str = Field(..., title="First name", alias="firstName")
    maternal_surname: str = Field(..., title="Maternal surname", alias='maternalSurname')
    paternal_surname: str = Field(..., title="Paternal surname", alias='paternalSurname')
    position: GeoLocationModel = Field(GeoLocationModel(), title="Current position", alias='position')


class DriverUser(CurrentUser):
    pass


class PassengerUser(CurrentUser):
    pass


class ScheduleData(BaseModel):
    price: int = Field(DEFAULT_PRICE, title="Max passengers", alias='maxPassengers')
    max_passengers: int = Field(4, title="Max passengers", alias='maxPassengers')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')

    @field_validator('price')
    def check_price(cls, price):
        if price < DEFAULT_MIN_PRICE:
            raise ValueError(f'The price cannot be less than ${price}')


class ScheduleTravelRequest(ScheduleData):
    origin: GeoLocationModel = Field(..., title="Location where the schedule begins", alias='start')
    destination: GeoLocationModel = Field(..., title="Location where the schedule ends", alias='end')


class ScheduleTravelFixedPointRequest(ScheduleData):
    a: GeoLocationModel = Field(..., alias='a')
    b: DefaultLocation = Field(DEFAULT_LOCATION, alias='b')

    return_home: bool = Field(..., title="Indicates whether the trip is a return home", alias='returnHome')

    @property
    def location(self) -> GeoLocationModel:
        latitude, longitude = get_gps_from_location(self.b)

        return GeoLocationModel(
            longitude=longitude,
            latitude=latitude,
        )

    @property
    def destination(self) -> GeoLocationModel:
        if self.return_home:
            return self.a

        return self.location

    @property
    def origin(self) -> GeoLocationModel:
        if self.return_home:
            return self.location

        return self.a


class ScheduleTravelResponse(BaseModel):
    uuid: UUID

    driver: DriverUser

    price: int

    terminate: bool = False
    cancel: bool = False

    starting: Optional[datetime] = Field(..., title="Time starting", alias='starting')
    terminated: Optional[datetime] = Field(..., title="Time finished", alias='terminated')

    max_passengers: int = Field(4, alias='maxPassengers')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')

    origin: GeoLocationModel
    destination: GeoLocationModel


class ScheduleTravelUpdateRequest(BaseModel):
    terminate: Optional[bool] = Field(None, alias='terminate')
    cancel: Optional[bool] = Field(None, alias='cancel')

    starting: Optional[datetime] = Field(None, title="Time starting", alias='starting')
