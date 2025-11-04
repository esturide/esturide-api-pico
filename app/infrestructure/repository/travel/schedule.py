from app.infrestructure.repository.client.cache import ClientCacheRepository
from app.shared.pattern.singleton import Singleton


class ScheduleRepository(ClientCacheRepository, metaclass=Singleton):
    async def search(self):
        pass
