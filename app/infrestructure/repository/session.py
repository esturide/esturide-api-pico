import contextlib

from beanie import Document


class AsyncSessionRepository:
    def __init__(self):
        pass

    async def save(self, instance: Document):
        return await instance.save() is not None

    async def update(self, instance: Document):
        return await instance.save() is not None

    @contextlib.asynccontextmanager
    async def session(self, instance: Document):
        yield instance

        await self.save(instance)
