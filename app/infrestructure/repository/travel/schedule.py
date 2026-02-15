from app.infrestructure.repository.client.cache import ClientCacheRepository
from app.shared.models.store.schedule import ScheduleStore
from app.shared.pattern.singleton import Singleton


class ScheduleStoreRepository(ClientCacheRepository, metaclass=Singleton):
    async def get(self, code: int) -> ScheduleStore | None:
        query = await ScheduleStore.find(ScheduleStore.usercode == code).sort_by("-created").all()

        if len(query) != 0:
            return query[0]

        return None
