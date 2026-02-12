import functools

from fastapi import BackgroundTasks

from app.infrestructure.repository.ride import RideCacheRepository
from app.shared.models.store.ride import RideStore
from app.shared.models.user import UserDocument
from app.shared.pattern.singleton import Singleton
from app.shared.scheme.rides import RideTravelRequest


class RideService(metaclass=Singleton):
    def __init__(self):
        self.ride_cache_repository = RideCacheRepository()

    async def create(self, user: UserDocument, req: RideTravelRequest, background_tasks: BackgroundTasks) -> bool:
        ride = await self.get_from_usercode(user.usercode)

        if ride:
            return False

        ride = RideStore(
            usercode=user.usercode,
            origin=req.origin,
            destination=req.destination,
            exiting=req.exiting,
            gender=user.gender
        )

        status = await self.ride_cache_repository.save(ride)

        return status

    async def get_from_usercode(self, usercode: str) -> RideStore | None:
        return await self.ride_cache_repository.get(usercode)

    async def get(self, code: str) -> RideStore | None:
        return await self.ride_cache_repository.get(code)


@functools.lru_cache
def get_ride_service():
    return RideService()
