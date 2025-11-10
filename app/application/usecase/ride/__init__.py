import asyncio
import contextlib
import functools
from typing import Optional

from fastapi import BackgroundTasks

from app.core.exception import NotFoundException, InvalidRequestException, ResourceNotFoundException
from app.domain.service.ride import RideService
from app.domain.service.schedule import ScheduleService
from app.domain.service.user import UserService
from app.shared.const import DEFAULT_MAX_RIDE_LIFETIME_SEC
from app.shared.models.ride import RideTravelModel
from app.shared.models.travel import ScheduleTravelDocument
from app.shared.models.user import User
from app.shared.pattern.singleton import Singleton
from app.shared.scheme import StatusFailure, StatusSuccess
from app.shared.scheme.respose.ride import create_ride_response
from app.shared.scheme.rides import RideTravelUpdateRequest, RideTravelRequest
from app.shared.scheme.rides.status import RideTravelStatusResponse
from app.shared.types import UUID
from app.shared.types.enum import RoleUser


class RideUseCase(metaclass=Singleton):
    def __init__(self):
        self.ride_service = RideService()
        self.schedule_service = ScheduleService()
        self.user_service = UserService()

    async def create(self, code: int, role: RoleUser, req: RideTravelRequest, background_tasks: BackgroundTasks):
        raise NotImplementedError()

    async def get_current_from_user(self, user: User) -> tuple[ScheduleTravelDocument | None, RideTravelModel | None]:
        raise NotImplementedError()

    async def find_ride_if_exist(self, code: int) -> Optional[RideTravelStatusResponse]:
        raise NotImplementedError()

    async def current(self, code: int) -> RideTravelStatusResponse:
        raise NotImplementedError()

    async def cancel(self, passenger: User, role: RoleUser, schedule: ScheduleTravelDocument, ride: RideTravelModel):
        raise NotImplementedError()

    async def over(self, passenger: User, role: RoleUser, schedule: ScheduleTravelDocument, ride: RideTravelModel):
        raise NotImplementedError()

    async def update(self, req: RideTravelUpdateRequest, code: int, role: RoleUser):
        raise NotImplementedError()

    async def notify(self, code: int, role: RoleUser, schedule_id: UUID):
        raise NotImplementedError()


@functools.lru_cache
def get_ride_use_case():
    return RideUseCase()
