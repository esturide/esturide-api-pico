import functools

from uuid import UUID

from app.domain.service.journeys.match import MatchService
from app.domain.service.journeys.ride import RideService
from app.domain.service.journeys.schedule import ScheduleTravelService
from app.domain.service.user import UserService
from app.shared.pattern.singleton import Singleton
from app.shared.scheme import StatusSuccess, StatusFailure


class MatchUseCase(metaclass=Singleton):
    def __init__(self):
        self.ride_service = RideService()
        self.schedule_service = ScheduleTravelService()
        self.match_service = MatchService()
        self.user_service = UserService()

    async def create(self, usercode: int, travel_schedule_id: UUID):
        passenger = await self.user_service.get(usercode)
        ride = await self.ride_service.get_from_usercode(usercode)
        travel_schedule = await self.schedule_service.get(travel_schedule_id)

        status = await self.match_service.create(passenger, ride, travel_schedule)

        if status:
            return StatusSuccess()

        return StatusFailure()

    async def search(self, usercode: int):
        return []

    async def check(self, usercode: int):
        yield StatusFailure()


@functools.lru_cache
def get_match_use_case():
    return MatchUseCase()
