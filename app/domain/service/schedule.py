import datetime
from typing import Set, List, Tuple, Optional

from pydantic import FutureDatetime

from app.core.exception import InvalidRequestException
from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.tracking import TrackingRepository
from app.infrestructure.repository.travel import TravelRepository
from app.infrestructure.repository.travel.schedule import ScheduleStoreRepository
from app.shared.models.ride import RideTravelModel
from app.shared.models.store.schedule import ScheduleStore
from app.shared.models.travel import ScheduleTravelDocument
from app.shared.models.user import UserDocument
from app.shared.pattern.singleton import Singleton
from app.shared.types import Seat, Gender


class ScheduleService(metaclass=Singleton):
    def __init__(self):
        self.ride_repository = RideRepository()
        self.schedule_store_repository = ScheduleStoreRepository()
        self.travel_repository = TravelRepository()
        self.tracking_repository = TrackingRepository()

    async def create(self, user: UserDocument, origin: str, destination: str, starting: FutureDatetime, price: float,
                     seats: Set[Seat], genders: Set[Gender], waypoints: Set[str],
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

    async def save(self, schedule: ScheduleStore) -> ScheduleTravelDocument | None:
        return

    async def get(self, code: int) -> List[ScheduleStore]:
        return await ScheduleStore.find(ScheduleStore.usercode == code).all()

    async def get_from_ride(self, ride: RideTravelModel) -> ScheduleTravelDocument | None:
        return

    async def get_current(self, user: UserDocument) -> ScheduleTravelDocument | None:
        return

    async def get_by_driver(self, user: UserDocument) -> list[ScheduleTravelDocument]:
        return []

    async def get_by_passenger(self, user: UserDocument) -> list[ScheduleTravelDocument]:
        return []

    async def all(self, limit=10) -> list[ScheduleTravelDocument]:
        return []

    async def filtering(self, origin: str, destination: str,
                        date: Tuple[datetime.datetime, Optional[datetime.datetime]],
                        price: Tuple[float, Optional[float]], limit: int) -> list[ScheduleTravelDocument]:
        min_price, max_price = price
        starting, finished = date

        if finished is None:
            finished = starting + datetime.timedelta(days=1)

        return await ScheduleStore.find(
            (
                    (ScheduleStore.origin % origin) | (ScheduleStore.destination % destination)
            ),
            (
                    (ScheduleStore.starting >= starting) & (ScheduleStore.terminated <= finished)
            )
        ).all()

    async def finished(self, schedule: ScheduleTravelDocument, cancel=None, terminate=None) -> tuple[bool, ScheduleTravelDocument] | None:
        return None
