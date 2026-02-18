from pydantic import BaseModel, FutureDatetime

from app.shared.types import Gender


class MatchTravelRequest(BaseModel):
    code: int


class MatchStatus(BaseModel):
    code: int
    accepted: bool


class MatchPassengerResult(BaseModel):
    code: int
    gender: Gender
    address: str

    starting: FutureDatetime
