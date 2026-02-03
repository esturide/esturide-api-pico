import uuid

from typing import Optional

from pydantic import BaseModel, Field


class RideTravelRequest(BaseModel):
    uuid: uuid.UUID
    seat: str


class RideTravelResponse(BaseModel):
    uuid: uuid.UUID

    seat: str
    cancel: bool
    over: bool
    accept: bool


class RideTravelUpdateRequest(BaseModel):
    over: Optional[bool] = Field(None, alias='over')
    cancel: Optional[bool] = Field(None, alias='cancel')
