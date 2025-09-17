import datetime
import functools

from geopy.geocoders.base import Geocoder
from google.cloud.firestore import GeoPoint

from app.domain.service.location.geo import search_from_address
from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.schedule import ScheduleRepository
from app.shared.models.ride import RideTravel
from app.shared.models.schedule import ScheduleTravel
from app.shared.models.user import User
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.schedule import ScheduleTravelFromAddressRequest
from app.shared.types import UUID


class ScheduleTravelService:
    async def create(self, geocoder: Geocoder, req: ScheduleTravelFromAddressRequest, user: User) -> ScheduleTravel | None:
        origin_address_result = await search_from_address(geocoder, req.origin)
        destination_address_result = await search_from_address(geocoder, req.destination)

        if len(origin_address_result) == 0 or len(destination_address_result) == 0:
            return None

        origin = origin_address_result[0]
        destination = destination_address_result[0]

        origin = GeoPoint(
            latitude=origin.latitude,
            longitude=origin.longitude,
        )

        destination = GeoPoint(
            latitude=destination.latitude,
            longitude=destination.longitude,
        )

        schedule = ScheduleTravel(
            driver=user,
            origin=origin,
            destination=destination,
            price=req.price,
            seats=req.seats,
        )

        schedule.rides = []
        schedule.tracking = []

        status = await ScheduleRepository.save(schedule)

        if status:
            return schedule

        return None

    async def get(self, uuid: UUID) -> ScheduleTravel:
        return await ScheduleRepository.get_from_uuid(uuid)

    async def get_from_ride(self, ride: RideTravel) -> ScheduleTravel | None:
        return await ScheduleRepository.get_current(ride=ride)

    async def get_current(self, user: User) -> ScheduleTravel | None:
        return await ScheduleRepository.get_current(user=user)

    async def get_by_driver(self, user: User) -> list[ScheduleTravel]:
        return await ScheduleRepository.get_by_driver(user)

    async def get_by_passenger(self, user: User) -> list[ScheduleTravel]:
        return await ScheduleRepository.get_by_passenger(user)

    async def all(self, limit=10) -> list[ScheduleTravel]:
        return await ScheduleRepository.get_all(limit)

    async def filtering(self, options: FilteringOptionsRequest, limit: int) -> list[ScheduleTravel]:
        return await ScheduleRepository.filtering(
            terminate=options.terminate,
            cancel=options.cancel,
            starting=options.starting,
            terminated=options.terminated,
            price_range=(options.min_price, options.max_price),
            order_date=options.order_by_date,
            limit=limit,
        )

    async def save(self, schedule: ScheduleTravel) -> bool:
        return await ScheduleRepository.update(schedule)

    async def finished(self, schedule: ScheduleTravel, cancel=None, terminate=None) -> tuple[bool, ScheduleTravel]:
        if terminate is not None:
            schedule.terminate = terminate
        elif cancel is not None:
            schedule.cancel = cancel

        schedule.terminated = datetime.datetime.now()

        if isinstance(schedule.rides, list):
            for rides in schedule.rides:
                rides.cancel = True
                await RideRepository.save(rides)

        status = await ScheduleRepository.save(schedule)

        return status, schedule


@functools.lru_cache
def get_schedule_service():
    return ScheduleTravelService()
