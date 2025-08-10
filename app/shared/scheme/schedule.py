from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.shared.scheme.location import DataGeoLocation
from app.shared.types import UUID


class CurrentUser(BaseModel):
    code: int
    first_name: str = Field(..., title="First name", alias="firstName")
    maternal_surname: str = Field(..., title="Maternal surname", alias='maternalSurname')
    paternal_surname: str = Field(..., title="Paternal surname", alias='paternalSurname')
    position: DataGeoLocation = Field(DataGeoLocation(), title="Current position", alias='position')


class DriverUser(CurrentUser):
    pass


class PassengerUser(CurrentUser):
    pass


class ScheduleTravelRequest(BaseModel):
    price: int = Field(5, title="Max passengers", alias='maxPassengers')
    max_passengers: int = Field(4, title="Max passengers", alias='maxPassengers')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')

    origin: DataGeoLocation = Field(..., title="Location where the schedule begins", alias='start')
    destination: DataGeoLocation = Field(..., title="Location where the schedule ends", alias='end')


class ScheduleTravelResponse(BaseModel):
    driver: DriverUser

    price: int

    terminate: bool = False
    cancel: bool = False

    starting: Optional[datetime] = Field(..., title="Time starting", alias='starting')
    terminated: Optional[datetime] = Field(..., title="Time finished", alias='terminated')

    max_passengers: int = Field(4, alias='maxPassengers')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')
    passengers: List[PassengerUser] = Field([], title="Passengers", alias='passengers')

    origin: DataGeoLocation
    destination: DataGeoLocation


class ScheduleTravelUpdateRequest(BaseModel):
    terminate: Optional[bool]
    cancel: Optional[bool]

    starting: Optional[datetime] = Field(..., title="Time starting", alias='starting')
    terminated: Optional[datetime] = Field(..., title="Time finished", alias='terminated')


class UserTrackingData(BaseModel):
    uuid: UUID
    record: DataGeoLocation


class RideStatusRequest(BaseModel):
    code: int
    validate: bool = True


class RideStatusResponse(PassengerUser):
    validate: bool = True


class RideRequest(BaseModel):
    origin: DataGeoLocation
    uuid: UUID = Field(..., alias='UUID')


class AuthTravelRequest(BaseModel):
    user_id: str
    trip_id: str


class RateRequest(BaseModel):
    user_id: str
    schedule_id: str
    overall: int = Field(..., ge=1, le=5)
    punctuality: int = Field(..., ge=1, le=5)
    driving_behavior: int = Field(..., ge=1, le=5)


class AutomobileRequest(BaseModel):
    code: int
    brand: str
    year: int
    model: str


class AutomobileResponse(BaseModel):
    code: int
    brand: str
    year: int
    model: str
