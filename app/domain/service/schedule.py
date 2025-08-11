import functools

from google.cloud.firestore import GeoPoint

from app.infrestructure.repository.schedule import ScheduleRepository
from app.shared.models.ride import RideTravel
from app.shared.models.schedule import ScheduleTravel
from app.shared.models.user import User
from app.shared.scheme.filter import FilteringOptionsRequest
from app.shared.scheme.schedule import ScheduleTravelRequest
from app.shared.types import UUID
from app.shared.types.enum import RoleUser


class ScheduleTravelService:
    async def create(self, req: ScheduleTravelRequest, user: User) -> bool:
        origin = GeoPoint(
            latitude=req.origin.latitude,
            longitude=req.origin.longitude,
        )

        destination = GeoPoint(
            latitude=req.destination.latitude,
            longitude=req.destination.longitude,
        )

        schedule = ScheduleTravel(
            driver=user,
            origin=origin,
            destination=destination,
            price=req.price,
            seats=req.seats,
        )

        return await ScheduleRepository.save(schedule)

    async def get(self, uuid: UUID) -> ScheduleTravel:
        return await ScheduleRepository.get_from_uuid(uuid)

    async def get_from_ride(self, ride: RideTravel) -> ScheduleTravel:
        return await ScheduleRepository.get_current(ride=ride)

    async def get_current(self, user: User, role: RoleUser = RoleUser.driver) -> ScheduleTravel:
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


@functools.lru_cache
def get_schedule_service():
    return ScheduleTravelService()
