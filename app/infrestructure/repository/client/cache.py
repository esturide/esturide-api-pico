import contextlib
import typing

from aredis_om import JsonModel, HashModel


class ClientCacheRepository:
    def __init__(self):
        self.expire_time_sec: typing.Optional[int] = None

    async def save(self, instance: JsonModel | HashModel, expire_time_sec=None):
        if expire_time_sec is not None:
            await instance.expire(self.expire_time_sec)
        elif self.expire_time_sec is not None:
            await instance.expire(self.expire_time_sec)

        return await instance.save() is not None

    async def update(self, instance: JsonModel | HashModel):
        return await instance.save() is not None

    @contextlib.asynccontextmanager
    async def session(self, instance: JsonModel | HashModel):
        yield instance

        await self.save(instance)
