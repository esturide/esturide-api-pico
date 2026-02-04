import contextlib
import functools
import uuid
from datetime import datetime
from typing import Optional

from fastapi import BackgroundTasks

from app.core.exception import NotFoundException
from app.infrestructure.repository.client.cache import ClientCacheRepository
from app.infrestructure.repository.ride import RideRepository, RideCacheRepository
from app.infrestructure.repository.travel import TravelRepository
from app.shared.models.ride import RideTravelModel
from app.shared.models.store.ride import RideStore
from app.shared.models.user import UserDocument
from app.shared.pattern.singleton import Singleton
from app.shared.scheme.rides import RideTravelRequest


class RideService(metaclass=Singleton):
    def __init__(self):
        self.ride_repository = RideRepository()
        self.ride_cache_repository = RideCacheRepository()
        self.schedule_repository = TravelRepository()

    async def create(self, user: UserDocument, req: RideTravelRequest, background_tasks: BackgroundTasks) -> bool:
        ride = RideStore(
            usercode=user.code,
            origin=req.origin,
            destination=req.destination,
            exiting=req.exiting,
            gender=user.gender
        )

        return await self.ride_cache_repository.save(ride)

    async def get_current_ride_from_user(self, passenger: UserDocument) -> RideTravelModel | None:
        all_rides = await self.get_all_rides_from_user(passenger)

        if len(all_rides) != 0 and all([rides.is_finished for rides in all_rides]):
            return None

        return all_rides[0]

    async def get_all_rides_from_user(self, passenger: UserDocument) -> list[RideTravelModel]:
        return await self.ride_repository.filter(passenger=passenger)

    async def get(self, uuid: uuid.UUID) -> RideTravelModel:
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
