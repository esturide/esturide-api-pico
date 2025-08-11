from typing import List

from pydantic import Field

from app.shared.scheme.rides.status import RidePassengerResponse
from app.shared.scheme.schedule import ScheduleTravelResponse


class ScheduleTravelStatusResponse(ScheduleTravelResponse):
    rides: List[RidePassengerResponse] = Field([], title="All current rides", alias='rides')
