import contextlib
import functools

from app.core.exception import NotFoundException
from app.infrestructure.repository.ride import RideRepository
from app.shared.models.ride import RideTravel
from app.shared.models.user import User
from app.shared.types import UUID


class RideService:
    async def create(self, passenger: User, seat: str) -> RideTravel:
        if seat not in ['A', 'B', 'C']:
            raise ""

        ride = RideTravel()

        ride.passenger = passenger
        ride.seat = seat

        await RideRepository.save(ride)

        return ride

    async def get_all_rides(self, passenger: User) -> list[RideTravel]:
        return await RideRepository.filter(passenger=passenger)

    async def get(self, uuid: UUID) -> RideTravel:
        ride =  await RideRepository.get(uuid)

        if ride is None:
            raise NotFoundException("Ride not found.")

        return ride

    async def save(self, ride: RideTravel):
        await RideRepository.save(ride)



@functools.lru_cache
def get_ride_service():
    return RideService()
