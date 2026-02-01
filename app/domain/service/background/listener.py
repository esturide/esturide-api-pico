import abc


class ListenerService:
    @abc.abstractmethod
    async def task(self):
        pass
