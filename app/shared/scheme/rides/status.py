from app.shared.scheme.rides import RideTravelResponse
from app.shared.scheme.schedule import ScheduleTravelResponse, PassengerUser


class RideTravelStatusResponse(RideTravelResponse):
    travel: ScheduleTravelResponse


class RidePassengerResponse(RideTravelResponse):
    passenger: PassengerUser
