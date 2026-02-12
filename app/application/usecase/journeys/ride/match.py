import functools

from app.core.exception import ResourceNotFoundException, UnauthorizedAccessException
from app.domain.service.journeys.match import MatchService
from app.domain.service.journeys.ride import RideService
from app.domain.service.journeys.schedule import ScheduleTravelService
from app.domain.service.user import UserService
from app.shared.pattern.singleton import Singleton
from app.shared.scheme import StatusSuccess, StatusFailure
from app.shared.scheme.match import MatchPassengerResult
from app.shared.scheme.schedule import ScheduleTravelResponse
from app.shared.types.enum import RoleUser


class MatchUseCase(metaclass=Singleton):
    def __init__(self):
        self.ride_service = RideService()
        self.schedule_service = ScheduleTravelService()
        self.match_service = MatchService()
        self.user_service = UserService()

    async def create(self, usercode: int, schedule_travel_code: int):
        passenger = await self.user_service.get(usercode)
        ride = await self.ride_service.get_from_usercode(usercode)
        travel_schedule = await self.schedule_service.get(schedule_travel_code)

        if not ride:
            return StatusFailure(message="Ride not found.")

        if not travel_schedule:
            return StatusFailure(message="Schedule travel not found.")

        if all((ride, travel_schedule)):
            status = await self.match_service.create(passenger, ride, travel_schedule)

            if status:
                return StatusSuccess()

        return StatusFailure(message="Cannot create match.")

    async def search(self, usercode: int):
        passenger = await self.user_service.get(usercode)
        ride = await self.ride_service.get_from_usercode(usercode)

        if ride is None:
            raise ResourceNotFoundException("Ride not found.")

        schedules = []

        for schedule in await self.schedule_service.filter(ride.destination, passenger.gender):
            schedules.append(ScheduleTravelResponse(
                code=schedule.usercode,
                origin=schedule.origin,
                destination=schedule.destination,
                starting=schedule.starting,
                price=schedule.price,
                genders=schedule.genders,
                waypoints=schedule.waypoints,
            ))

        return schedules

    async def check(self, usercode: int):
        yield StatusFailure()

    async def review(self, usercode: int, role: RoleUser):
        if role != RoleUser.driver:
            raise UnauthorizedAccessException("You need become driver.")

        driver = await self.user_service.get(usercode)
        schedule = await self.schedule_service.get(usercode)

        if schedule is None:
            raise ResourceNotFoundException("Schedule travel not found.")

        all_match = []

        for match in await self.match_service.get_all_from_schedule(schedule):
            passenger = await self.user_service.get(match.code)
            ride = await self.ride_service.get(match.code)

            all_match.append(MatchPassengerResult(
                code=match.code,
                gender=passenger.gender,
                address=ride.address,
                starting=ride.exiting
            ))

        return all_match


@functools.lru_cache
def get_match_use_case():
    return MatchUseCase()
