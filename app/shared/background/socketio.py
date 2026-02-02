import asyncio
import functools

from app.shared.pattern.singleton import Singleton

class AsyncClientConnectionManager(metaclass=Singleton):
    def __init__(self):
        self.__sid = {}

    def attach(self, sid: str):
        def inner(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                await func(*args, **kwargs)

            task = asyncio.create_task(wrapper())
            self.__sid[sid] = task

            return task

        return inner

    async def detach(self, sid: str):
        if sid in self.__sid and not self.__sid[sid].done():
            self.__sid[sid].cancel()

            await self.__sid[sid]

        return None
