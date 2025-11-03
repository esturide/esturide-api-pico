import datetime
import functools

from geopy.geocoders.base import Geocoder

from app.domain.service.location.geolocation import search_from_address
from app.domain.service.location.geolocation.search import search_location_from_address
from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.schedule import ScheduleRepository
from app.infrestructure.repository.tracking import TrackingRepository
from app.shared.models.location import LocationModel
from app.shared.models.ride import RideTravelModel
from app.shared.models.schedule import ScheduleTravelModel
from app.shared.models.tracking import Tracking
from app.shared.models.user import User
from app.shared.pattern.singleton import Singleton
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.location import GeoPoint
from app.shared.scheme.schedule import ScheduleTravelFromAddressRequest


class ScheduleTravelService(metaclass=Singleton):
    def __init__(self):
        self.ride_repository = RideRepository()
        self.schedule_repository = ScheduleRepository()
        self.tracking_repository = TrackingRepository()

    async def create(self, geocoder: Geocoder, req: ScheduleTravelFromAddressRequest,
                     user: User) -> ScheduleTravelModel | None:
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

        tracking = Tracking()
        await self.tracking_repository.save(tracking)

        schedule = ScheduleTravelModel(
            driver=user,
            origin=origin,
            destination=destination,
            price=req.price,
            seats=req.seats,
            gender_filter=req.gender_filter,
            waypoints=waypoints,
            tracking=tracking
        )

        status = await self.schedule_repository.save(schedule)

        if status:
            return schedule

        return None

    async def get(self, code: int) -> ScheduleTravelModel:
        return await self.schedule_repository.get_from_code(code)

    async def get_from_ride(self, ride: RideTravelModel) -> ScheduleTravelModel | None:
        return await self.schedule_repository.get_current(ride=ride)

    async def get_current(self, user: User) -> ScheduleTravelModel | None:
        schedule = await self.schedule_repository.get_current(user=user)

        if schedule is None:
            return None

        if schedule.lifetime_exceeded:
            schedule.cancel = True
            await self.save(schedule)

        return schedule

    async def get_by_driver(self, user: User) -> list[ScheduleTravelModel]:
        return await self.schedule_repository.get_by_driver(user)

    async def get_by_passenger(self, user: User) -> list[ScheduleTravelModel]:
        return await self.schedule_repository.get_by_passenger(user)

    async def all(self, limit=10) -> list[ScheduleTravelModel]:
        return await self.schedule_repository.get_all(limit)

    async def filtering(self, options: FilteringOptionsRequest, limit: int) -> list[ScheduleTravelModel]:
        return await self.schedule_repository.filtering(
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
        return await self.schedule_repository.update(schedule)

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

        status = await self.schedule_repository.save(schedule)

        return status, schedule


@functools.lru_cache
def get_schedule_service():
    return ScheduleTravelService()
