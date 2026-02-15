from typing import Set, List, Tuple

from pydantic import FutureDatetime

from app.core.exception import InvalidRequestException
from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.tracking import TrackingRepository
from app.infrestructure.repository.travel import TravelRepository
from app.infrestructure.repository.travel.schedule import ScheduleStoreRepository
from app.shared.models.store.schedule import ScheduleStore
from app.shared.models.user import UserDocument
from app.shared.pattern.singleton import Singleton
from app.shared.types import Seat, Gender


class ScheduleTravelService(metaclass=Singleton):
    def __init__(self):
        self.ride_repository = RideRepository()
        self.schedule_store_repository = ScheduleStoreRepository()
        self.travel_repository = TravelRepository()
        self.tracking_repository = TrackingRepository()

    async def create(self, user: UserDocument, origin: str, destination: str, starting: FutureDatetime, price: float,
                     seats: Set[Seat], genders: Set[Gender], waypoints: Set[str],
                     route: List[Tuple[float, float]]) -> ScheduleStore | None:
        previous_schedule_found = await self.schedule_store_repository.get(user.code)

        if previous_schedule_found is not None:
            raise InvalidRequestException("A previous schedule was found, it cannot be rescheduled.")

        if not user.is_valid_driver:
            raise InvalidRequestException('User is not an approved driver.')

        schedule = ScheduleStore(
            usercode=user.usercode,
            origin=origin,
            destination=destination,
            starting=starting,
            price=price,
            seats=seats,
            genders=genders,
            waypoints=waypoints,
            route=route
        )

        await self.schedule_store_repository.save(schedule)

        return schedule

    async def get_from_user(self, usercode: int) -> ScheduleStore | None:
        return await self.schedule_store_repository.get(usercode)

    async def get(self, code: int) -> ScheduleStore | None:
        return await self.schedule_store_repository.get(code)

    async def get_from_destination(self, destination: str) -> list[ScheduleStore]:
        return await ScheduleStore.find(ScheduleStore.destination == destination).all()

    async def filter(self, destination: str, gender: Gender) -> list[ScheduleStore]:
        return await ScheduleStore.find(
            (ScheduleStore.destination == destination) | (ScheduleStore.genders >> gender)
        ).all()
