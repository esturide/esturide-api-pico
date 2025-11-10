import datetime
import functools
from typing import Set, List, Tuple

from app.core.exception import InvalidRequestException
from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.tracking import TrackingRepository
from app.infrestructure.repository.travel import TravelRepository
from app.infrestructure.repository.travel.schedule import ScheduleStoreRepository
from app.shared.models.ride import RideTravelModel
from app.shared.models.store.schedule import ScheduleStore
from app.shared.models.travel import ScheduleTravelDocument
from app.shared.models.user import User
from app.shared.pattern.singleton import Singleton
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.types import SeatOption, Gender


class ScheduleService(metaclass=Singleton):
    def __init__(self):
        self.ride_repository = RideRepository()
        self.schedule_store_repository = ScheduleStoreRepository()
        self.travel_repository = TravelRepository()
        self.tracking_repository = TrackingRepository()

    async def create(self, user: User, origin: str, destination: str, starting: datetime.datetime, price: float,
                     seats: Set[SeatOption], genders: Set[Gender], waypoints: Set[str],
                     route: List[Tuple[float, float]]):
        previous_schedule_found = await ScheduleStore.find(ScheduleStore.usercode == user.code).all()

        if len(previous_schedule_found) != 0:
            raise InvalidRequestException("A previous schedule was found, it cannot be rescheduled.")

        if not user.is_valid_driver:
            raise InvalidRequestException('User is not an approved driver.')

        schedule = ScheduleStore(
            usercode=user.code,
            origin=origin,
            destination=destination,
            starting=starting,
            price=price,
            seats=seats,
            genders=genders,
            waypoints=waypoints,
            route=route
        )

        await self.schedule_store_repository.save(schedule, expire_time_sec=120)

        return schedule

    async def get(self, code: int) -> List[ScheduleStore]:
        return await ScheduleStore.find(ScheduleStore.usercode == code).all()

    async def get_from_ride(self, ride: RideTravelModel) -> ScheduleTravelDocument | None:
        return

    async def get_current(self, user: User) -> ScheduleTravelDocument | None:
        return

    async def get_by_driver(self, user: User) -> list[ScheduleTravelDocument]:
        return []

    async def get_by_passenger(self, user: User) -> list[ScheduleTravelDocument]:
        return []

    async def all(self, limit=10) -> list[ScheduleTravelDocument]:
        return []

    async def filtering(self, options: FilteringOptionsRequest, limit: int) -> list[ScheduleTravelDocument]:
        return []

    async def save(self, schedule: ScheduleTravelDocument) -> bool:
        return False

    async def finished(self, schedule: ScheduleTravelDocument, cancel=None, terminate=None) -> tuple[bool, ScheduleTravelDocument] | None:
        return None
