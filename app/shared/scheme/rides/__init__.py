import datetime

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.shared.types.enum.default_location import DefaultLocation


class RideTravelRequest(BaseModel):
    origin: str | DefaultLocation = Field(..., title="Location where the travel begins", alias='origin')
    destination: str | DefaultLocation = Field(..., title="Location where the travel ends", alias='destination')

    exiting: datetime.datetime = Field(..., title="Date and time when the trip begins", alias='exiting')


class RideTravelResponse(BaseModel):
    uuid: UUID

    seat: str
    cancel: bool
    over: bool
    accept: bool


class RideTravelUpdateRequest(BaseModel):
    over: Optional[bool] = Field(None, alias='over')
    cancel: Optional[bool] = Field(None, alias='cancel')
