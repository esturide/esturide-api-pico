import functools

from app.domain.service.journeys.ride import RideService
from app.domain.service.journeys.schedule import ScheduleTravelService
from app.domain.service.user import UserService
from app.shared.pattern.singleton import Singleton


class MatchUseCase(metaclass=Singleton):
    def __init__(self):
        self.ride_service = RideService()
        self.schedule_service = ScheduleTravelService()
        self.user_service = UserService()

    async def search(self, usercode: int):
        ride = await self.ride_service.get_from_usercode(usercode)

    async def create(self):
        pass

    async def accept(self):
        pass


@functools.lru_cache
def get_match_use_case():
    return MatchUseCase()
