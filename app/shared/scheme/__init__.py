from typing import List, TypeVar, Generic

from pydantic import BaseModel, Field

from app.shared.types.enum import Status

T = TypeVar('T')


class StatusResponse(BaseModel, Generic[T]):
    status: Status = Field(..., title="Status response")
    data: List[T] | T


class StatusMessage(BaseModel):
    status: Status = Field(..., title="Status response")
    message: str = Field(..., title="Message response")


class StatusSuccess(StatusMessage):
    status: Status = Status.success
    message: str = "Success."


class StatusFailure(StatusMessage):
    status: Status = Status.failure
    message: str = "Failure."
