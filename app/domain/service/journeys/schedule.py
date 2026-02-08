import datetime

from typing import Set, List, Tuple, Optional
from uuid import UUID

from pydantic import FutureDatetime

from app.core.exception import InvalidRequestException
from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.tracking import TrackingRepository
from app.infrestructure.repository.travel import TravelRepository
from app.infrestructure.repository.travel.schedule import ScheduleStoreRepository
from app.shared.models.store.schedule import ScheduleStore
from app.shared.models.travel import TravelDocument
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
                     route: List[Tuple[float, float]]) -> Optional[ScheduleStore]:
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

    async def save(self, schedule: ScheduleStore) -> TravelDocument | None:
        return None

    async def get(self, uuid: UUID):
        if query := await ScheduleStore.find(ScheduleStore.uuid == uuid).all():
            return query[0]

        return None

    async def get_from_user(self, usercode: int) -> ScheduleStore | None:
        if query := await ScheduleStore.find(ScheduleStore.usercode == usercode).all():
            return query[0]

        return None

    async def get_current(self, user: UserDocument) -> TravelDocument | None:
        return None

    async def get_by_driver(self, user: UserDocument) -> list[TravelDocument]:
        return []

    async def get_by_passenger(self, user: UserDocument) -> list[TravelDocument]:
        return []

    async def all(self, limit=10) -> list[TravelDocument]:
        return []

    async def filtering(self, origin: str, destination: str,
                        date: Tuple[datetime.datetime, Optional[datetime.datetime]],
                        price: Tuple[float, Optional[float]], limit: int) -> list[TravelDocument]:
        return []

    async def finished(self, schedule: TravelDocument, cancel=None, terminate=None) -> tuple[bool, TravelDocument] | None:
        return None
