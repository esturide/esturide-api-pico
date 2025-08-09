from typing import List, TypeVar, Generic

from pydantic import BaseModel, Field

from app.types.enum import Status

T = TypeVar('T')


class StatusResponse(BaseModel, Generic[T]):
    data: List[T] | T
    status: Status = Field(..., title="Status response")


class StatusMessage(BaseModel):
    status: Status = Field(..., title="Status response")
    message: str = Field(..., title="Message response")
