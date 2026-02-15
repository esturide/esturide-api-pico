import datetime

from aredis_om import JsonModel, Field

from app.shared.dependencies.depends.cache import get_async_client_redis
from app.shared.types import Seat, Gender


class RideStore(JsonModel, index=True):
    usercode: int = Field(index=True, const=True)

    created: datetime.datetime = Field(default_factory=datetime.datetime.now, index=True, const=True)

    origin: str = Field(..., index=True, const=True)
    destination: str = Field(..., index=True, const=True)
    exiting: datetime.datetime = Field(..., index=True, const=True)

    gender: Gender = Field(..., const=True)

    class Meta:
        database = get_async_client_redis()

    @property
    def code(self) -> int:
        return int(self.usercode)

    @property
    def address(self):
        return self.origin

    @property
    def starting(self):
        return self.exiting
