import functools
import uuid

from fastapi import BackgroundTasks

from app.core.exception import NotFoundException
from app.infrestructure.repository.ride import RideRepository, RideCacheRepository
from app.infrestructure.repository.travel import TravelRepository
from app.shared.models.store.ride import RideStore
from app.shared.models.user import UserDocument
from app.shared.pattern.singleton import Singleton
from app.shared.scheme.rides import RideTravelRequest


class RideService(metaclass=Singleton):
    def __init__(self):
        self.ride_cache_repository = RideCacheRepository()

    async def create(self, user: UserDocument, req: RideTravelRequest, background_tasks: BackgroundTasks) -> bool:
        usercode = user.code
        ride = await self.get_from_usercode(usercode)

        if ride:
            return False

        ride = RideStore(
            usercode=user.code,
            origin=req.origin,
            destination=req.destination,
            exiting=req.exiting,
            gender=user.gender
        )

        status = await self.ride_cache_repository.save(ride)

        return status

    async def get_from_usercode(self, usercode: int) -> RideStore | None:
        rides = await RideStore.find(RideStore.usercode == usercode).sort_by("-created").all()

        if len(rides) >= 1:
            return rides[0]

        return None

    async def get(self, uuid: uuid.UUID) -> RideStore | None:
        rides = await RideStore.find(RideStore.uuid == uuid).sort_by("-created").all()

        if len(rides) >= 1:
            return rides[0]

        return None

    async def delete(self, uuid: uuid.UUID):
        ride = await self.get(uuid)


@functools.lru_cache
def get_ride_service():
    return RideService()
