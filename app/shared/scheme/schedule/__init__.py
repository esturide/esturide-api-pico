import datetime
from typing import Optional, Set

import pytz
from pydantic import BaseModel, Field, field_validator, model_validator, FutureDatetime

from app.shared.const import DEFAULT_MIN_PRICE
from app.shared.scheme.location import GeoPoint
from app.shared.types import UUID, Seat
from app.shared.types.enum import Gender
from app.shared.types.enum.default_location import DefaultLocation, get_gps_from_location


class CurrentUser(BaseModel):
    code: int
    first_name: str = Field(..., title="First name", alias="firstName")
    maternal_surname: str = Field(..., title="Maternal surname", alias='maternalSurname')
    paternal_surname: str = Field(..., title="Paternal surname", alias='paternalSurname')
    position: GeoPoint = Field(..., title="Current position", alias='position')


class DriverUser(CurrentUser):
    pass


class PassengerUser(CurrentUser):
    pass


class ScheduleTravelFromAddressRequest(BaseModel):
    origin: str | DefaultLocation = Field(..., title="Location where the travel begins", alias='origin')
    destination: str | DefaultLocation = Field(..., title="Location where the travel ends", alias='destination')
    return_home: Optional[bool] = Field(default=None, title="Indicates whether the trip is a return home",
                                        alias='returnHome')

    starting: datetime.datetime = Field(..., title="Date and time when the trip begins", alias='starting')

    price: int = Field(DEFAULT_MIN_PRICE, title="Price of the travel", alias='price')
    seats: Set[Seat] = Field(['A', 'B', 'C'], title="All seats", alias='seats')
    genders: Set[Gender] = Field(["male", "female"], title="Filter of genders", alias='genders')

    waypoints: Set[str] = Field(..., title="Ride waypoints", alias='waypoints')

    @classmethod
    @field_validator('starting')
    def validate_starting_schedule_time(cls, v: datetime.datetime) -> datetime.datetime:
        local_time = pytz.timezone('America/Mexico_City')

        if v.tzinfo is None:
            v = local_time.localize(v)
        else:
            v = v.astimezone(local_time)

        now = datetime.datetime.now(datetime.timezone.utc)
        minimum_value = now + datetime.timedelta(hours=1)

        if v < minimum_value:
            raise ValueError('The date must be at least one hour later than the current one.')

        return v

    @classmethod
    @field_validator('gender_filter')
    def check_gender(cls, gender: list[Gender]):
        if len(gender) > 2:
            raise ValueError("There seems to be an error regarding the number of filters.")
        elif len(gender) == 0:
            raise ValueError('You cannot start a trip with these filters.')

        return gender

    @classmethod
    @field_validator('price')
    def check_price(cls, price: int):
        if price < DEFAULT_MIN_PRICE:
            raise ValueError(f'The price cannot be less than ${price}')

        return price

    @model_validator(mode="after")
    def check_address_if_same(self):
        if self.origin == self.destination:
            raise ValueError("The address cannot be the same.")

        return self

    @property
    def address_from_default_location(self) -> tuple[float, float]:
        if self.return_home and self.origin in DefaultLocation:
            return get_gps_from_location(DefaultLocation(self.origin))
        elif not self.return_home and self.destination in DefaultLocation:
            return get_gps_from_location(DefaultLocation(self.destination))

        raise ValueError("Invalid location.")

    @property
    def max_passengers(self):
        return len(self.seats)


class ScheduleTravelResponse(BaseModel):
    uuid: UUID
    driver: DriverUser

    price: int

    terminate: bool = False
    cancel: bool = False

    starting: Optional[datetime.datetime] = Field(..., title="Time starting", alias='starting')
    terminated: Optional[datetime.datetime] = Field(..., title="Time finished", alias='terminated')

    seats: Set[Seat] = Field(['A', 'B', 'C'], title="All seats", alias='seats')

    origin: str
    destination: str

    genders: Set[Gender] = Field(..., title="Filter of genders", alias='genders')

    waypoints: Set[str]


class ScheduleTravelUpdateRequest(BaseModel):
    terminate: Optional[bool] = Field(default=None, alias='terminate')
    cancel: Optional[bool] = Field(default=None, alias='cancel')

    starting: Optional[datetime.datetime] = Field(default=None, title="Time starting", alias='starting')
