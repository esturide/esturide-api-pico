import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator, FutureDatetime

from app.shared.const import DEFAULT_MIN_PRICE
from app.shared.scheme.location import GeoLocationModel, GeoLocationAddressModel
from app.shared.types import UUID
from app.shared.types.enum import Gender
from app.shared.types.enum.default_location import DefaultLocation, get_gps_from_location


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


class ScheduleTravelFromAddressRequest(BaseModel):
    origin: str | DefaultLocation = Field(..., title="Location where the schedule begins", alias='origin')
    destination: str | DefaultLocation = Field(..., title="Location where the schedule ends", alias='destination')
    return_home: bool = Field(..., title="Indicates whether the trip is a return home", alias='returnHome')

    start_date: FutureDatetime = Field(..., title="Date and time when the trip begins", alias='startDate')

    price: int = Field(DEFAULT_MIN_PRICE, title="Price of the travel", alias='price')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')

    gender_filter: List[Gender] = Field(["male", "female"], title="Filter of genders", alias='genderFilter')

    @field_validator('gender_filter')
    @classmethod
    def check_gender(cls, gender: list[Gender]):
        if len(gender) > 2:
            raise ValueError("There seems to be an error regarding the number of filters.")
        elif len(gender) == 0:
            raise ValueError('You cannot start a trip with these filters.')

        return gender

    @field_validator('price')
    @classmethod
    def check_price(cls, price: int):
        if price < DEFAULT_MIN_PRICE:
            raise ValueError(f'The price cannot be less than ${price}')

        return price

    @model_validator(mode="after")
    def check_address_if_same(self):
        if self.origin == self.destination:
            raise ValueError("The address cannot be the same.")

        return self

    @model_validator(mode="after")
    def check_if_valid_address(self):
        if self.return_home and self.origin not in DefaultLocation:
            raise ValueError("You can't return home from that direction.")
        elif not self.return_home and self.destination not in DefaultLocation:
            raise ValueError("You can't go to that address if you leave the house.")

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

    max_passengers: int = Field(4, alias='maxPassengers')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')

    origin: GeoLocationAddressModel
    destination: GeoLocationAddressModel

    gender_filter: list[Gender] = Field(..., title="Filter of genders", alias='genderFilter')


class ScheduleTravelUpdateRequest(BaseModel):
    terminate: Optional[bool] = Field(default=None, alias='terminate')
    cancel: Optional[bool] = Field(default=None, alias='cancel')

    starting: Optional[datetime.datetime] = Field(default=None, title="Time starting", alias='starting')
