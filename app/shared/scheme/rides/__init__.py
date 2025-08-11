from pydantic import BaseModel

from app.shared.scheme.schedule import ScheduleTravelResponse
from app.shared.types import UUID


class RideTravelResponse(BaseModel):
    uuid: UUID

    seat: str
    cancel: bool
    over: bool
    accept: bool

    travel: ScheduleTravelResponse
