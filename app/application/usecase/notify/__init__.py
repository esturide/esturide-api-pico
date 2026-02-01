import functools

from app.domain.service.ride import RideService
from app.domain.service.schedule import ScheduleService
from app.domain.service.user import UserService
from app.shared.const import DEFAULT_DELAY_TIME_NOTIFY
from app.shared.types.enum import RoleUser


class NotifyUseCase:
    def __init__(self):
        self.user_service = UserService()
        self.ride_service = RideService()
        self.schedule_service = ScheduleService()
        self.time_sleep = DEFAULT_DELAY_TIME_NOTIFY

    async def notify_ride(self, code: int, role: RoleUser):
        pass

    async def notify_schedule(self, code: int, role: RoleUser):
        pass


@functools.lru_cache
def get_notify_user_case():
    return NotifyUseCase()
