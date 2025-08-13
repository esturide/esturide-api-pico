import asyncio
import functools

from app.domain.service.ride import get_ride_service
from app.domain.service.schedule import get_schedule_service
from app.domain.service.user import get_user_service
from app.shared.const import DEFAULT_DELAY_TIME_NOTIFY
from app.shared.scheme.respose.ride import create_ride_response
from app.shared.scheme.respose.schedule import create_schedule_status_response
from app.shared.types.enum import RoleUser


class NotifyUseCase:
    def __init__(self):
        self.user_service = get_user_service()
        self.ride_service = get_ride_service()
        self.schedule_service = get_schedule_service()
        self.time_sleep = DEFAULT_DELAY_TIME_NOTIFY

    async def notify_ride(self, code: int, role: RoleUser):
        user = await self.user_service.get(code)

        while True:
            ride = await self.ride_service.get_current_ride_from_user(user)
            schedule = await self.schedule_service.get_from_ride(ride)

            yield create_ride_response(schedule, ride)

            await asyncio.sleep(self.time_sleep)

    async def notify_schedule(self, code: int, role: RoleUser):
        user = await self.user_service.get(code)

        while True:
            schedule = await self.schedule_service.get_current(user)

            yield create_schedule_status_response(schedule)

            await asyncio.sleep(self.time_sleep)


@functools.lru_cache
def get_notify_user_case():
    return NotifyUseCase()
