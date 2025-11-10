import datetime
import functools
from typing import Set, List, Tuple

from app.core.exception import InvalidRequestException
from app.domain.service.location.geolocation import search_from_address
from app.domain.service.location.geolocation.search import search_location_from_address
from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.travel import TravelRepository
from app.infrestructure.repository.tracking import TrackingRepository
from app.infrestructure.repository.travel.schedule import ScheduleStoreRepository
from app.shared.models.ride import RideTravelModel
from app.shared.models.store.schedule import ScheduleStore
from app.shared.models.travel import ScheduleTravelModel
from app.shared.models.tracking import Tracking
from app.shared.models.user import User
from app.shared.pattern.singleton import Singleton
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.schedule import ScheduleTravelFromAddressRequest
from app.shared.types import SeatOption, Gender


class ScheduleTravelService(metaclass=Singleton):
    def __init__(self):
        self.ride_repository = RideRepository()
        self.schedule_store_repository = ScheduleStoreRepository()
        self.travel_repository = TravelRepository()
        self.tracking_repository = TrackingRepository()

    async def create(self, user: User, origin: str, destination: str, starting: datetime.datetime, price: float, seats: Set[SeatOption], genders: Set[Gender], waypoints: Set[str], route: List[Tuple[float, float]]):
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

    async def get(self, code: int) -> ScheduleTravelModel:
        return await self.travel_repository.get_from_code(code)

    async def get_from_ride(self, ride: RideTravelModel) -> ScheduleTravelModel | None:
        return await self.travel_repository.get_current(ride=ride)

    async def get_current(self, user: User) -> ScheduleTravelModel | None:
        schedule = await self.travel_repository.get_current(user=user)

        if schedule is None:
            return None

        if schedule.lifetime_exceeded:
            schedule.cancel = True
            await self.save(schedule)

        return schedule

    async def get_by_driver(self, user: User) -> list[ScheduleTravelModel]:
        return await self.travel_repository.get_by_driver(user)

    async def get_by_passenger(self, user: User) -> list[ScheduleTravelModel]:
        return await self.travel_repository.get_by_passenger(user)

    async def all(self, limit=10) -> list[ScheduleTravelModel]:
        return await self.travel_repository.get_all(limit)

    async def filtering(self, options: FilteringOptionsRequest, limit: int) -> list[ScheduleTravelModel]:
        return await self.travel_repository.filtering(
            terminate=options.terminate,
            cancel=options.cancel,
            starting=options.starting,
            terminated=options.terminated,
            price_range=(options.min_price, options.max_price),
            order_date=options.order_by_date,
            limit=limit,
            seats=options.seats
        )

    async def save(self, schedule: ScheduleTravelModel) -> bool:
        return await self.travel_repository.update(schedule)

    async def finished(self, schedule: ScheduleTravelModel, cancel=None, terminate=None) -> tuple[bool, ScheduleTravelModel]:
        if terminate is not None:
            schedule.terminate = terminate
        elif cancel is not None:
            schedule.cancel = cancel

        schedule.terminated = datetime.datetime.now()

        if isinstance(schedule.rides, list):
            for rides in schedule.rides:
                rides.cancel = True
                await self.ride_repository.save(rides)

        status = await self.travel_repository.save(schedule)

        return status, schedule


@functools.lru_cache
def get_schedule_service():
    return ScheduleTravelService()
