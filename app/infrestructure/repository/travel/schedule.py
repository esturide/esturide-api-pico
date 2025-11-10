from app.infrestructure.repository.client.cache import ClientCacheRepository
from app.shared.pattern.singleton import Singleton


class ScheduleStoreRepository(ClientCacheRepository, metaclass=Singleton):
    async def search(self):
        pass
