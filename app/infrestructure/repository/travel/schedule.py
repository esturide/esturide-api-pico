from app.infrestructure.repository.client.cache import ClientCacheRepository
from app.shared.models.store.schedule import ScheduleStore
from app.shared.pattern.singleton import Singleton


class ScheduleStoreRepository(ClientCacheRepository, metaclass=Singleton):
    async def get(self, code: int) -> ScheduleStore | None:
        schedules = await ScheduleStore.find().sort_by("-created").all()
        schedules = list(filter(lambda s: s.usercode == code, schedules))

        if len(schedules) != 0:
            return schedules[0]

        return None
