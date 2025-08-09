from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from app.shared.scheme.location import DataAddressLocation
from app.shared.types import UUID


class TrackingRecord(BaseModel):
    latitude: float = 0
    longitude: float = 0


class DriverUser(BaseModel):
    code: int

    first_name: str = Field(..., title="firstName", alias="firstName")
    maternal_surname: str = Field(..., title="Maternal surname", alias='maternalSurname')
    paternal_surname: str = Field(..., title="Paternal surname", alias='paternalSurname')
    position: TrackingRecord = Field(TrackingRecord(), title="Current position", alias='position')


class PassengerUser(BaseModel):
    code: int

    first_name: str = Field(..., title="firstName", alias="firstName")
    maternal_surname: str = Field(..., title="Maternal surname", alias='maternalSurname')
    paternal_surname: str = Field(..., title="Paternal surname", alias='paternalSurname')
    position: TrackingRecord = Field(TrackingRecord(), title="Current position", alias='position')


class ScheduleTravelRequest(BaseModel):
    start: DataAddressLocation = Field(..., title="Location where the schedule begins", alias='start')
    end: DataAddressLocation = Field(..., title="Location where the schedule ends", alias='end')
    price: int = Field(5, title="Max passengers", alias='maxPassengers')
    max_passengers: int = Field(4, title="Max passengers", alias='maxPassengers')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')


class TravelScheduleResponse(BaseModel):
    uuid: UUID

    driver: DriverUser

    price: int
    active: bool = False
    terminate: bool = False
    cancel: bool = False

    starting: datetime = Field(..., title="Time starting", alias='starting')
    finished: datetime = Field(..., title="Time finished", alias='finished')

    max_passengers: int = Field(4, alias='maxPassengers')
    seats: List[str] = Field(['A', 'B', 'C'], title="All seats", alias='seats')
    passengers: List[PassengerUser] = Field([], title="Passengers", alias='passengers')

    origin: DataAddressLocation
    destination: DataAddressLocation


class Tracking(BaseModel):
    uuid: UUID
    record: TrackingRecord


class RideStatusRequest(BaseModel):
    code: int
    validate: bool = True


class RideStatusResponse(PassengerUser):
    validate: bool = True


class RideRequest(BaseModel):
    origin: TrackingRecord
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
