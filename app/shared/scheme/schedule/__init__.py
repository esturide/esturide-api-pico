from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from app.shared.const import DEFAULT_PRICE, DEFAULT_MIN_PRICE
from app.shared.scheme.location import GeoLocationModel
from app.shared.types import UUID


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


class ScheduleTravelRequest(BaseModel):
    price: int = Field(DEFAULT_PRICE, title="Max passengers", alias='maxPassengers')
    max_passengers: int = Field(4, title="Max passengers", alias='maxPassengers')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')

    origin: GeoLocationModel = Field(..., title="Location where the schedule begins", alias='start')
    destination: GeoLocationModel = Field(..., title="Location where the schedule ends", alias='end')

    @field_validator('price')
    def check_price(cls, price):
        if price < DEFAULT_MIN_PRICE:
            raise ValueError(f'The price cannot be less than ${price}')

        return price


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
