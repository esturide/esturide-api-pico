from pydantic import BaseModel, Field

from app.shared.scheme.rides import RideTravelResponse
from app.shared.scheme.schedule import ScheduleTravelResponse, PassengerUser
from app.shared.types.enum.ride import RideStatus


class RideTravelStatusResponse(RideTravelResponse):
    travel: ScheduleTravelResponse


class RidePassengerResponse(RideTravelResponse):
    passenger: PassengerUser


class CurrentRideStatus(BaseModel):
    status: RideStatus = Field(default=RideStatus.waiting)
