from typing import Optional

from pydantic import BaseModel, Field

from app.shared.types import UUID


class RideTravelRequest(BaseModel):
    uuid: UUID
    seat: str


class RideTravelResponse(BaseModel):
    uuid: UUID

    seat: str
    cancel: bool
    over: bool
    accept: bool


class RideTravelUpdateRequest(BaseModel):
    over: Optional[bool] = Field(None, alias='over')
    cancel: Optional[bool] = Field(None, alias='cancel')
