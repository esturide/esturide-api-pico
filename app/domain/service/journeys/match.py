from app.infrestructure.repository.match import MatchRepository
from app.shared.models.store.match import MatchStore
from app.shared.models.store.ride import RideStore
from app.shared.models.store.schedule import ScheduleStore
from app.shared.models.user import UserDocument
from app.shared.pattern.singleton import Singleton


class MatchService(metaclass=Singleton):
    def __init__(self) -> None:
        self.match_repository = MatchRepository()

    async def create(self, passenger: UserDocument, ride: RideStore, schedule: ScheduleStore) -> None:
        match = MatchStore(
            usercode=passenger.code,
            ride_id=ride.uuid,
            travel_schedule_id=schedule.uuid
        )

        return await self.match_repository.save(match)
