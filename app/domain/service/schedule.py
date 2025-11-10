import datetime
import functools
from typing import Set

from app.domain.service.location.geolocation import search_from_address
from app.domain.service.location.geolocation.search import search_location_from_address
from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.travel import TravelRepository
from app.infrestructure.repository.tracking import TrackingRepository
from app.infrestructure.repository.travel.schedule import ScheduleRepository
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
        self.schedule_repository = ScheduleRepository()
        self.travel_repository = TravelRepository()
        self.tracking_repository = TrackingRepository()

    async def create(self, user: User, origin: str, destination: str, starting: datetime.datetime, price: float, seats: Set[SeatOption], genders: Set[Gender], waypoints: Set[str]):
        schedule = ScheduleStore(
            usercode=user.code,
            origin=origin,
            destination=destination,
            starting=starting,
            price=price,
            seats=seats,
            genders=genders,
            waypoints=waypoints,
            route=[(0, 0)]
        )

        await schedule.save()
        await schedule.expire(120)

    async def old_create(self, geocoder, req: ScheduleTravelFromAddressRequest, user: User) -> ScheduleTravelModel | None:
        origin_address_result = await search_location_from_address(geocoder, req.origin)
        destination_address_result = await search_location_from_address(geocoder, req.destination)

        if len(origin_address_result) == 0 or len(destination_address_result) == 0:
            return None

        origin, _ = origin_address_result[0]
        destination, _ = destination_address_result[0]

        waypoints = set()

        for waypoint in req.waypoints:
            address, (latitude, longitude) = await search_from_address(geocoder, waypoint)
            waypoints.add(address)

        tracking = Tracking(records=[])
        await self.tracking_repository.save(tracking)

        schedule = ScheduleTravelModel(
            driver=user,
            origin=origin,
            destination=destination,
            price=req.price,
            seats=req.seats,
            gender_filter=req.genders,
            waypoints=waypoints,
            tracking=tracking
        )

        status = await self.travel_repository.save(schedule)

        if status:
            return schedule

        return None

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
