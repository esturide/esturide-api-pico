from pydantic import BaseModel

from app.shared.types import UUID


class ChangesScheduleRequest(BaseModel):
    uuid: UUID

    cancel: bool
    terminate: bool
