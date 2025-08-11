from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

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
    price: int = Field(5, title="Max passengers", alias='maxPassengers')
    max_passengers: int = Field(4, title="Max passengers", alias='maxPassengers')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')

    origin: GeoLocationModel = Field(..., title="Location where the schedule begins", alias='start')
    destination: GeoLocationModel = Field(..., title="Location where the schedule ends", alias='end')


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
    terminate: Optional[bool]
    cancel: Optional[bool]

    starting: Optional[datetime] = Field(..., title="Time starting", alias='starting')
    terminated: Optional[datetime] = Field(..., title="Time finished", alias='terminated')
