from typing import List

from pydantic import Field

from app.shared.scheme.rides import RideTravelResponse
from app.shared.scheme.schedule import ScheduleTravelResponse


class ScheduleTravelStatusResponse(ScheduleTravelResponse):
    rides: List[RideTravelResponse] = Field([], title="Passengers", alias='passengers')

