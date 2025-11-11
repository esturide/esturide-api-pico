import contextlib
import functools

from app.core.exception import NotFoundException
from app.infrestructure.repository.ride import RideRepository
from app.infrestructure.repository.travel import TravelRepository
from app.shared.models.ride import RideTravelModel
from app.shared.models.user import UserDocument
from app.shared.pattern.singleton import Singleton
from app.shared.types import UUID


class RideService(metaclass=Singleton):
    def __init__(self):
        self.ride_repository = RideRepository()
        self.schedule_repository = TravelRepository()

    async def create(self, passenger: UserDocument, seat: str) -> RideTravelModel:
        if seat not in ['A', 'B', 'C']:
            raise ""

        ride = RideTravelModel()

        ride.passenger = passenger
        ride.seat = seat
        ride.tracking = []

        await self.ride_repository.save(ride)

        return ride

    async def get_current_ride_from_user(self, passenger: UserDocument) -> RideTravelModel | None:
        all_rides = await self.get_all_rides_from_user(passenger)

        if len(all_rides) != 0 and all([rides.is_finished for rides in all_rides]):
            return None

        return all_rides[0]

    async def get_all_rides_from_user(self, passenger: UserDocument) -> list[RideTravelModel]:
        return await self.ride_repository.filter(passenger=passenger)

    async def get(self, uuid: UUID) -> RideTravelModel:
        ride = await self.ride_repository.get(uuid)

        if ride is None:
            raise NotFoundException("Ride not found.")

        return ride

    async def save(self, ride: RideTravelModel):
        await self.ride_repository.save(ride)

    @contextlib.asynccontextmanager
    async def update(self, ride: RideTravelModel):
        yield ride

        await self.save(ride)


@functools.lru_cache
def get_ride_service():
    return RideService()
