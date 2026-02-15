from aredis_om import Field, HashModel

from app.shared.dependencies.depends.cache import get_async_client_redis


class MatchStore(HashModel, index=True):
    usercode: int = Field(primary_key=True, const=True)

    ride_code: str = Field(index=True, const=True)
    travel_schedule_code: str = Field(index=True, const=True)

    accepted: bool = Field(default=False)
    denegated: bool = Field(default=False)

    class Meta:
        database = get_async_client_redis()

    @property
    def code(self) -> int:
        return int(self.usercode)
