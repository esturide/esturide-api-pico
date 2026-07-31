import uuid

from pydantic import BaseModel



class ChangesScheduleRequest(BaseModel):
    uuid: uuid.UUID

    cancel: bool
    terminate: bool
