import functools
from typing import Optional
from uuid import UUID

from fastapi import BackgroundTasks

from app.domain.service.journeys.ride import RideService
from app.domain.service.journeys.schedule import ScheduleTravelService
from app.domain.service.user import UserService
from app.shared.models.ride import RideTravelModel
from app.shared.models.travel import ScheduleTravelDocument
from app.shared.models.user import UserDocument
from app.shared.pattern.singleton import Singleton
from app.shared.scheme.rides import RideTravelUpdateRequest, RideTravelRequest
from app.shared.scheme.rides.status import RideTravelStatusResponse
from app.shared.types.enum import RoleUser
from app.shared.scheme import StatusSuccess, StatusFailure, StatusMessage


class RideUseCase(metaclass=Singleton):
    def __init__(self):
        self.ride_service = RideService()
        self.schedule_service = ScheduleTravelService()
        self.user_service = UserService()

    async def create(self, usercode: int, role: RoleUser, req: RideTravelRequest, background_tasks: BackgroundTasks) -> StatusMessage:
        if not role == RoleUser.passenger:
            return StatusFailure(
                    message="You can not request a ride."
            )

        user = await self.user_service.get(usercode)
        status = await self.ride_service.create(user, req, background_tasks)

        if status:
            return StatusSuccess(
                message="Ride is created."
            )
        else:
            return StatusFailure(
                    message="Failure creating Ride."
            )

    async def get_current_from_user(self, user: UserDocument) -> tuple[
        ScheduleTravelDocument | None, RideTravelModel | None]:
        raise NotImplementedError()

    async def exist(self, usercode: int) -> bool:
        return False

    async def current(self, usercode: int) -> Optional[RideTravelStatusResponse]:
        raise NotImplementedError()

    async def cancel(self, passenger: UserDocument, role: RoleUser, schedule: ScheduleTravelDocument,
                     ride: RideTravelModel):
        raise NotImplementedError()

    async def over(self, passenger: UserDocument, role: RoleUser, schedule: ScheduleTravelDocument,
                   ride: RideTravelModel):
        raise NotImplementedError()

    async def update(self, req: RideTravelUpdateRequest, code: int, role: RoleUser):
        raise NotImplementedError()

    async def notify(self, code: int, role: RoleUser, schedule_id: UUID):
        raise NotImplementedError()


@functools.lru_cache
def get_ride_use_case():
    return RideUseCase()
