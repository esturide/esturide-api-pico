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
            ride_code=ride.usercode,
            travel_schedule_code=schedule.usercode
        )

        return await self.match_repository.save(match)

    async def get_all_from_schedule(self, schedule: ScheduleStore) -> list[MatchStore]:
        code = schedule.usercode
        match_schedule = await MatchStore.find(MatchStore.travel_schedule_code == code).all()

        return match_schedule
