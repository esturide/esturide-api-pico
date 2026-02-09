import uuid

from uuid import UUID

from aredis_om import Field, HashModel


class MatchStore(HashModel, index=True):
    uuid: UUID = Field(default_factory=uuid.uuid4, index=True, const=True)

    usercode: int = Field(..., const=True)

    ride_id: UUID = Field(index=True, const=True)
    travel_schedule_id: UUID = Field(index=True, const=True)

    accepted: bool = Field(default=False)
    denegated: bool = Field(default=False)
